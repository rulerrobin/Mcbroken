# report schema
from init import db, ma
from marshmallow import fields
from datetime import datetime

# Add association tables for upvotes and downvotes
report_upvotes = db.Table(
    'report_upvotes',
    db.Column('report_id', db.Integer, db.ForeignKey('reports.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

report_downvotes = db.Table(
    'report_downvotes',
    db.Column('report_id', db.Integer, db.ForeignKey('reports.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)


class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    time_reported = db.Column(db.DateTime, default=datetime.utcnow) # Time and date posted
    broken = db.Column(db.Boolean, default=False)
    upvotes = db.Column(db.Integer, default=0) 
    downvotes = db.Column(db.Integer, default=0) 

    # Foreign Keys
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    # Do cascade deletes later for links
    # Relationships
    location = db.relationship('Location', back_populates='reports', cascade='all, delete')

    user = db.relationship('User', back_populates='reports', cascade='all, delete')

    comments = db.relationship('Comment', back_populates='report', cascade='all, delete')

# Returning userSchema is only for admins unless searched username is same as user
class ReportSchema(ma.Schema):

    # Schema Connections
    location = fields.Nested('LocationSchema')
    user = fields.Nested('UserSchema', exclude=['id', 'email', 'password', 'is_admin'])
    comments = fields.List(fields.Nested('CommentSchema', exclude=['id']))

    # Formats time to readable string
    time_reported = fields.DateTime(format='%Y-%m-%d %H:%M:%S')

    # Fields for upvotes and downvotes

    class Meta:
        fields = ('id','broken','location','user','time_reported','upvotes', 'downvotes', 'comments')