# user model and schema 
from init import db, ma


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Do cascade deletes later for links

    # Relationships
    reports = db.relationship('Report', backref='user', cascade='all, delete')
    comments = db.relationship('Comment', backref='user', cascade='all, delete')


# Returning userSchema is only for admins unless searched username is same as user
class UserSchema(ma.Schema):

    # possible future version will have reputation

    class Meta:
        fields = ('username', 'email', 'password', 'is_admin')