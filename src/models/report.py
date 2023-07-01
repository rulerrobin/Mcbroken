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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    # Do cascade deletes later for links
    # Relationships
    location = db.relationship('Location', back_populates='reports', cascade='all, delete')
    user = db.relationship('User', back_populates='reports', cascade='all, delete')
    comments = db.relationship('Comment', back_populates='report', cascade='all, delete')
    votes = db.relationship('Vote', backref='report')

# Returning userSchema is only for admins unless searched username is same as user
class ReportSchema(ma.Schema):

    # Schema Connections
    location = fields.Nested('LocationSchema')
    user = fields.Nested('UserSchema', exclude=['id', 'email', 'password', 'is_admin'])
    comments = fields.List(fields.Nested('CommentSchema', exclude=['id']))

    # Formats time to readable string
    time_reported = fields.DateTime(format='%Y-%m-%d %H:%M:%S')

    # add a field for votes
    upvotes = fields.Method("get_upvotes")
    downvotes = fields.Method("get_downvotes")

    # Count the votes
    def get_upvotes(self, obj):
        return len([vote for vote in obj.votes if vote.vote_type == "upvote"])

    def get_downvotes(self, obj):
        return len([vote for vote in obj.votes if vote.vote_type == "downvote"])



    class Meta:
        fields = ('id','broken','location','user','time_reported', 'comments', 'upvotes', 'downvotes')