# Register, login, seed

from flask import Blueprint
from datetime import date
from models.user import User
from init import db, bcrypt

cli_bp = Blueprint('db', __name__) # unique name, typically __name__ dunder

@cli_bp.cli.command('create') # Create tables
    def create_db():