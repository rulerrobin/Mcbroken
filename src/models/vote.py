# vote model and schema
from init import db, ma
from marshmallow import fields

class Vote(db.Model):
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    vote_type = db.Column(db.String(10), nullable=False)  # 'upvote' or 'downvote'

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id', ondelete='CASCADE'))

    # Relationships
    user = db.relationship('User', backref='votes')
    report = db.relationship('Report', backref='votes')

class VoteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'vote_type', 'user', 'report')
