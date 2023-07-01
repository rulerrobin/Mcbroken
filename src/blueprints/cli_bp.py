# commands

from flask import Blueprint
from datetime import datetime
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

@cli_bp.cli.command('seed') # Fills tables with predetermined values
def seed_db():

    users = [
        User(
            username = 'admin',
            email = 'admin@gmail.com',
            password = bcrypt.generate_password_hash('admin123').decode('utf-8'),
            is_admin = True
        ),        
        User(
            username = 'Jonny',
            email = 'jonny@gmail.com',
            password = bcrypt.generate_password_hash('jon123').decode('utf-8'),
            is_admin = False
        ),
        User(
            username = 'Jane',
            email = 'jane@gmail.com',
            password = bcrypt.generate_password_hash('jane123').decode('utf-8'),
            is_admin = False
        )        
    ]

    db.session.query(User).delete() # Cascade delete as reports are connected to users and comments to users and reports
    db.session.add_all(users) # add changes
    db.session.commit() # Commit Changes

    # Create Location Seed
    locations = [
        Location (
            number = '600',
            street = 'George Street',
            postcode = '2000',
            suburb = 'Sydney',
            state =  'NSW',
        ),
        Location (
            number = '183',
            street = 'Botany Road',
            postcode = '2000',
            suburb = 'Sydney',
            state =  'NSW',
        ),      
        Location (
            number = 'G2/620',
            street = 'Collins Street',
            postcode = '3000',
            suburb = 'Melbourne',
            state =  'Victoria',
        )           
    ]

    db.session.query(Location).delete()
    db.session.add_all(locations) # add changes
    db.session.commit() # Commit Changes


    # Create Reports Seeds
    reports = [
        Report (
            time_reported=datetime.utcnow(),
            broken = False,
            user=users[0],
            location=locations[0]
        ),
        Report (
            time_reported=datetime.utcnow(),
            broken = True,
            user=users[1],
            location=locations[1]
        ),        
        Report (
            time_reported=datetime.utcnow(),
            broken = False,
            user=users[2],
            location=locations[2]
        )                
    ]

    db.session.query(Report).delete()
    db.session.add_all(reports) # add changes
    db.session.commit() # Commit Changes

    # Create Comment Seeds
    comments = [
        Comment (
            comment = 'This place never breaks down. It"s the best place to get soft serves!',
            time_posted = datetime.utcnow(),
            user = users[0],
            report = reports[0]
        ),
        Comment (
            comment = 'Worst place to get soft serves...',
            time_posted = datetime.utcnow(),
            user = users[2],
            report = reports[1]
        ),
        Comment (
            comment = 'It finally works...',
            time_posted = datetime.utcnow(),
            user = users[1],
            report = reports[2]
        )
    ]

    db.session.query(Comment).delete()
    db.session.add_all(comments) # add changes
    db.session.commit() # Commit Changes

    print ('Models seeded')