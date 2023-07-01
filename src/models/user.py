# user model and schema 
from init import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


    # Add columns for upvoted and downvoted reports
    upvoted_reports = db.relationship('Report', secondary='report_upvotes', backref='upvoters') # join tables are in report.py
    downvoted_reports = db.relationship('Report', secondary='report_downvotes', backref='downvoters')

    # Relationships
    reports = db.relationship('Report', back_populates='user')
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete')


# Returning userSchema is only for admins unless searched username is same as user
class UserSchema(ma.Schema):

    # possible future version will have reputation

    class Meta:
        fields = ('id', 'username', 'email', 'password', 'is_admin')
