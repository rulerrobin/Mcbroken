# comment schema
from init import db, ma
from marshmallow import fields
from datetime import datetime


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    time_posted = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    # Do cascade deletes later for links

    # Relationships
    report = db.relationship('Report', back_populates='comments', cascade='all, delete')


# Returning userSchema is only for admins unless searched username is same as user
class CommentSchema(ma.Schema):

    user = fields.Nested('UserSchema', only=['username'])

    class Meta:
        fields = ('id', 'user','comment','date_created', 'time_posted')