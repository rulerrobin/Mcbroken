# commands

from flask import Blueprint
from datetime import date
from models.user import User
from models.report import Report
from init import db, bcrypt
from models.comment import Comment
from models.location import Location

cli_bp = Blueprint('db', __name__)

@cli_bp.cli.command('create') # Creates new tables after dropping tables and comimits
def create_db():
    db.drop_all() # Drops all tables
    db.create_all() # Creates all databases that are defined
    db.session.commit() # commits changes
    print('Tables Created Successfully') # Print Checking

    