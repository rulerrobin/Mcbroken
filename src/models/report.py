# report schema
from init import db, ma
from marshmallow import fields
from datetime import datetime

class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    time_reported = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Keys
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Do cascade deletes later for links
    # Relationships
    location = db.relationship('Location', back_populates='reports', cascade='all, delete')
    user = db.relationship('User', back_populates='reports', cascade='all, delete')

# Returning userSchema is only for admins unless searched username is same as user
class ReportSchema(ma.Schema):

    # Schema Connections

    # Location first as to show where 
    location = fields.List(fields.Nested('LocationSchema'))
    comments = fields.List(fields.Nested('CommentSchema', exclude=['id']))
    user = fields.Nested('UserSchema', only=('username'))

    class Meta:
        fields = ('id','user','time_reported', 'comments')