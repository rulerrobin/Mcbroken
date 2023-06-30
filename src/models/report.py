# report schema
from init import db, ma
from marshmallow import fields
from datetime import datetime

class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    time_reported = db.Column(db.DateTime, default=datetime.utcnow) # Time and date posted
    broken = db.Column(db.Boolean, default=False)

    # Foreign Keys
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    

    # Do cascade deletes later for links
    # Relationships
    location = db.relationship('Location', back_populates='reports', cascade='all, delete')
    user = db.relationship('User', backref='reports', cascade='all, delete')
    comments = db.relationship('Comment', backref='report', cascade='all, delete')

# Returning userSchema is only for admins unless searched username is same as user
class ReportSchema(ma.Schema):

    # Schema Connections
    location = fields.List(fields.Nested('LocationSchema'))
    user = fields.Nested('UserSchema', exclude=['id', 'email', 'password', 'is_admin'])
    comments = fields.List(fields.Nested('CommentSchema', exclude=['id']))

    class Meta:
        fields = ('id', 'location','user','time_reported', 'comments')