# create and update reports

from flask import Blueprint, request, jsonify
from sqlalchemy import join, desc, and_
from models.report import Report, ReportSchema
from models.location import Location
from models.user import User
from models.vote import Vote
from models.comment import Comment, CommentSchema
from init import db, jwt
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from .auth_bp import admin_or_owner_required

reports_bp = Blueprint('report', __name__, url_prefix='/reports')

def report_not_found_error():
    return {"error": "Report not found"}, 400 

def voted():
    return {"error": "You have already voted this report"}, 400

@reports_bp.route('/') # Get all reports
def all_reports():
    stmt = db.select(Report)
    reports = db.session.scalars(stmt).all() 

    return ReportSchema(many=True).dump(reports) 

# Suburb Filter
@reports_bp.route('/suburb/<string:suburb>')
def suburb_filter(suburb):
    # Join table to get all locations in a certain suburb
    stmt = db.select(Report).select_from(join(Report, Location)).where(Location.suburb==suburb)
    reports = db.session.execute(stmt).scalars().all()
    return ReportSchema(many=True).dump(reports)

# Broken Machine Filter
@reports_bp.route('/broken')
def broken_machines():
    stmt = db.select(Report).filter_by(broken=True)
    reports = db.session.scalars(stmt).all()
    return ReportSchema(many=True).dump(reports)

# Working Machine Filter
@reports_bp.route('/working')
def working_machines():
    stmt = db.select(Report).filter_by(broken=False)
    reports = db.session.scalars(stmt).all()
    return ReportSchema(many=True).dump(reports)

# Report Machine
@reports_bp.route('/report', methods=['POST'])
@jwt_required()
def report_machine():
    try:
        # Machine Details
        report_info = ReportSchema().load(request.json)
        
        report = Report(
            broken=report_info['broken'],  # ID and Time are auto completed
            user_id=get_jwt_identity(),  # To get user id to link since user is logged in
        )

        # Location Details
        location_data = request.json['location']
        existing_location = Location.query.filter_by(
            number=location_data['number'],
            street=location_data['street'],
            postcode=location_data['postcode'],
            suburb=location_data['suburb'],
            state=location_data['state']
        ).first()

        if existing_location: # IF location combination exists returns and gives error
            return {'error': 'Report already exists for this location, please search using /reports/suburb/"suburb Mcdonald\s is from"'}, 409

        # Location adding if above is False
        location = Location(
            number=location_data['number'],
            street=location_data['street'],
            postcode=location_data['postcode'],
            suburb=location_data['suburb'],
            state=location_data['state']
        )        

        report.location = location
        db.session.add(report)
        db.session.commit()

        return 'Broken machine report added successfully'
    except Exception as e:
        # Handle other exceptions
        return {'error': str(e)}, 500
    

# Update Report
@reports_bp.route('/<int:report_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_report(report_id):
 
    report = Report.query.get(report_id) # Gets report with report id

    if not report: 
        report_not_found_error()

    # Time check if 15 minutes have passed since last update/creation
    time_threshold = report.time_reported + timedelta(minutes=1) # Checks what is report time + 15 minutes and puts in time_threshold
    if datetime.utcnow() < time_threshold: # compares time_threshold to current time and if over current time then update
        update_time = time_threshold.strftime("%Y-%m-%d %H:%M:%S") # Format time as string
        return {"error": f"Cannot update the report. Next update available at: {update_time}"}, 400 # Return error and when it can be updated

    # Update the report 
    report_info = ReportSchema().load(request.json)
    report.broken = report_info['broken'] # Update boolean value

    # Update report/update time
    report.time_reported = datetime.utcnow() # With current time

    # Reset Votes
    Vote.query.filter_by(report_id=report_id).delete()

    # Update the user who made the update
    current_user_id = get_jwt_identity() # Get user_id from JWT Token
    current_user = User.query.get(current_user_id) # Get user from db
    report.user = current_user # gets current user

    db.session.commit()

    return {"Message": "Report has been updated successfully"}, 201

@reports_bp.route('/<int:report_id>/upvote', methods=['POST'])
@jwt_required()
def upvote_report(report_id):
    report = Report.query.get(report_id) # gets report 

    if not report:
        return report_not_found_error()

    current_user_id = get_jwt_identity()

    # Check if the user has already upvoted or downvoted the report
    existing_vote = Vote.query.filter_by(report_id=report_id, user_id=current_user_id).first()

    if existing_vote:
        if existing_vote.vote_type == 'upvote':
            return {"message": "Already upvoted"}
        else:
            # Remove the downvote
            db.session.delete(existing_vote)

    # Create a new Vote record for the upvote
    vote = Vote(vote_type='upvote', user_id=current_user_id, report_id=report_id)
    db.session.add(vote)

    db.session.commit()

    return {"message": "Upvote successful"}, 201

@reports_bp.route('/<int:report_id>/downvote', methods=['POST'])
@jwt_required()
def downvote_report(report_id):
    report = Report.query.get(report_id)

    if not report:
        return report_not_found_error()

    current_user_id = get_jwt_identity()

    # Check if the user has already upvoted or downvoted the report
    existing_vote = Vote.query.filter_by(report_id=report_id, user_id=current_user_id).first()

    if existing_vote:
        if existing_vote.vote_type == 'downvote':
            return {"message": "Already downvoted"}
        else:
            # Remove the upvote
            db.session.delete(existing_vote)

    # Create a new Vote record for the downvote
    vote = Vote(vote_type='downvote', user_id=current_user_id, report_id=report_id)
    db.session.add(vote)

    db.session.commit()

    return {"message": "Downvote successful"}, 201

# Comments

@reports_bp.route('/<int:report_id>/comment', methods=['POST'])
@jwt_required()
def create_comment(report_id):
    report = Report.query.get(report_id)

    if not report:
        return report_not_found_error()
    
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    # Get the comment data from the request
    comment_info = request.json
    
    # Create comment
    comment = Comment (
        comment = comment_info ['comment'],
        time_posted = datetime.utcnow(),
        user = current_user,
        report = report
    )

    db.session.add(comment)
    db.session.commit()

    return 'Comment posted added successfully'

# Edit commments
@reports_bp.route('/<int:report_id>/comment/<int:comment_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def delete_comment(report_id):
    report = Report.query.get(report_id)

    if not report:
        return report_not_found_error()
    
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    # Get the comment data from the request
    comment_info = request.json
    
    # Create comment
    comment = Comment (
        comment = comment_info ['comment'],
        time_posted = datetime.utcnow(),
        user = current_user,
        report = report
    )

    db.session.add(comment)
    db.session.commit()

    return 'Comment posted added successfully'