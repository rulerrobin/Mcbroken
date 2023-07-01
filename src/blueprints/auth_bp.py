# Register, login, seed

from flask import Blueprint, request, abort, Flask
from datetime import date, timedelta
from models.user import User, UserSchema
from sqlalchemy.exc import IntegrityError
from init import db, bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

cli_bp = Blueprint('db', __name__) # unique name, typically __name__ dunder
auth_bp = Blueprint('auth', __name__, url_prefix='/users') 

def admin_required():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not (user and user.is_admin):
        abort(401, description='You must be an admin')

def admin_or_user_required(username):
    user = User.query.filter_by(username=username).first() # Filters by username and gets first matching (unique)

    if not (user and (user.is_admin or user.username == get_jwt_identity())):
        abort(401, description="You must be an admin or the user")


@auth_bp.route('/')
@jwt_required()
def all_users():
    admin_required() # checks if admin otherwise aborted and given a 401 error
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    return UserSchema(many=True, exclude=['password']).dump(users)

@auth_bp.route('/<string:username>')
@jwt_required()
def search_user(username):
    stmt = db.select(User).filter_by(username=username)
    user = db.session.scalar(stmt)
    if user:
        return UserSchema(exclude=['password', 'email', 'is_admin']).dump(user)
    else: 
        return {'error':'User not found'}, 404
    

@auth_bp.route('/register', methods=['POST']) # Register for account
def register():
    try:
        user_info = UserSchema().load(request.json) # Loads the Post request into JSON usermodel instance

        # fill user model with incoming request data
        user = User(
            username = user_info['username'],
            email = user_info['email'],
            password = bcrypt.generate_password_hash(user_info['password']).decode('utf-8'),      
        )

        # Add and commit user to db
        db.session.add(user)
        db.session.commit()
        
        # Returns new user if successful

        return UserSchema(exclude=['password']).dump(user), 201
    except IntegrityError:
        if 'email' in str(e):
            return {'error': 'Email address already in use'}, 409
        elif 'username' in str(e):
            return {'error': 'Username already in use'}, 409


# Login to account
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        stmt = db.select(User).filter_by(username=request.json['username']) # Filter by username to login
        user = db.session.scalar(stmt)

        if user and bcrypt.check_password_hash(user.password, request.json['password']): # Checks user is true and password is correct
            token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
            return {'token': token, 'user': UserSchema(exclude=['password']).dump(user)}
        else:
            return {'error': 'Invalid email address or password'}, 401        
    except KeyError:
        return {'error': 'Email and password are required'}, 400

# @auth_bp.route('/')


        