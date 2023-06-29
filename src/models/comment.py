# comment schema
from init import db, ma
from marshmallow import fields
from datetime import datetime


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    time_posted = db.Column(db.DateTime, default=datetime.utcnow)

    # Do cascade deletes later for links

# Returning userSchema is only for admins unless searched username is same as user
class CommentSchema(ma.Schema):


    class Meta:
        fields = ('comment', 'time_posted', 'password')