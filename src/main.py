from flask import Flask
from init import db, ma, bcrypt, jwt
from os import environ
from blueprints.cli_bp import cli_bp

def setup():

    app = Flask(__name__)

    app.config['JWT_KEY'] = environ.get('JWT_KEY')

    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(cli_bp)

    return app
