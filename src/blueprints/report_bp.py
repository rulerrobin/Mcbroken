# create and update reports

from flask import Blueprint, request, jsonify
from models.report import Report, ReportSchema
from models.location import Location
from models.user import User
from init import db, jwt
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError

reports_bp = Blueprint('report', __name__, url_prefix='/reports')

@reports_bp.route('/') # Get all reports
def all_reports():
    stmt = db.select(Report)
    reports = db.session.scalars(stmt).all() 
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
            return {'error': 'Address recently reported'}, 409

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
        error_message = {"error": "Report not found"}
        return jsonify(error_message), 404

    # Time check if 15 minutes have passed since last update/creation
    time_threshold = report.time_reported + timedelta(minutes=15) # Checks what is report time + 15 minutes and puts in time_threshold
    if datetime.utcnow() < time_threshold: # compares time_threshold to current time and if over current time then update
        update_time = time_threshold.strftime("%Y-%m-%d %H:%M:%S") # Format time as string
        return {"error": f"Cannot update the report. Next update available at: {update_time}"}, 400 # Return error and when it can be updated

    # Update the report 
    report_info = ReportSchema().load(request.json)
    report.broken = report_info['broken'] # Update boolean value

    # Update report/update time
    report.time_reported = datetime.utcnow() # With current time

    # Update the user who made the update
    current_user_id = get_jwt_identity() # Get user_id from JWT Token
    current_user = User.query.get(current_user_id) # Get user from db
    report.user = current_user # gets current user

    db.session.commit()

    return {"Message": "Report has been updated successfully"}
