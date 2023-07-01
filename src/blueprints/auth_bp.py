# Register, login, seed

from flask import Blueprint, request, abort
from datetime import timedelta
from models.user import User, UserSchema
from models.comment import Comment
from sqlalchemy.exc import IntegrityError
from init import db, bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

cli_bp = Blueprint('db', __name__) # unique name, typically __name__ dunder
auth_bp = Blueprint('auth', __name__, url_prefix='/users') 

def unauthorised_error():
    return {'error': 'You must be an admin or the user'}, 401

def admin_required():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not (user and user.is_admin):
        raise Exception("You must be an admin")

def admin_or_user_required():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not (user and (user.is_admin or user_id == user.id)):
        unauthorised_error()
       

@auth_bp.route('/<string:username>', methods=['DELETE'])
@jwt_required()
def delete_user(username):
    stmt = db.select(User).filter_by(username=username)
    user = db.session.scalar(stmt)
    if user:
        try:
            admin_or_user_required()

            # Delete user comment
            Comment.query.filter_by(user_id=user.id).delete()
            
            db.session.delete(user)
            db.session.commit()
            return {'Message': 'User deleted successfully'}, 200
        except Exception as e:
            abort(401, description=str(e))

    else:
        return {'Error': 'User not found'}, 404
    
# View all users admin required
@auth_bp.route('/')
@jwt_required()
def all_users():
    try:
        admin_required() # checks if admin otherwise aborted and given a 401 error
        stmt = db.select(User)
        users = db.session.scalars(stmt)
        return UserSchema(many=True, exclude=['password']).dump(users)
    except Exception as e:
            abort(401, description=str(e))

# View users if name available
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

        return {"Message": "Registration Successful", "user" : UserSchema(exclude=['password', 'is_admin']).dump(user)}, 201
    except IntegrityError as e:
        if 'email' in str(e) and 'username' in str(e):
            return {'error': 'Email address and username already in use'}, 409
        elif 'username' in str(e):
            return {'error': 'Username already in use'}, 409
        elif 'email' in str(e):
            return {'error': 'Email address already in use'}, 409        


# Login to account
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        stmt = db.select(User).filter_by(username=request.json['username']) # Filter by username to login
        user = db.session.scalar(stmt)

        if user and bcrypt.check_password_hash(user.password, request.json['password']): # Checks user is true and password is correct
            token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
            return {'token': token, 'user': UserSchema(exclude=['password', 'comments']).dump(user)}
        else:
            return {'error': 'Invalid email address or password'}, 401        
    except KeyError:
        return {'error': 'Email and password are required'}, 400



        