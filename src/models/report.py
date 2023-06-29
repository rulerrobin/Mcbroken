# report schema
from init import db, ma
from marshmallow import fields
from datetime import datetime

class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True)
    time_reported = db.Column(db.DateTime, default=datetime.utcnow)

    # Do cascade deletes later for links

# Returning userSchema is only for admins unless searched username is same as user
class ReportSchema(ma.Schema):
    users = fields.List(fields.Nested('UserSchema', exclude=['email', 'password']))

    class Meta:
        fields = ('time_reported', 'users')