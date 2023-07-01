# create and update reports

from flask import Blueprint, request, abort
from models.report import Report, ReportSchema
from models.location import Location, LocationSchema
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date
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

    stmt = db.select(Report).filter_by(id=report_id)
    report = db.session.scalar(stmt)
    report_info = ReportSchema().load(request.json)

    report.broken = report_info['broken']
    time_reported = date.today() ['time_reported']
    db.session.commit() # no add as just aditing existing
    return ReportSchema().dump(report)     
