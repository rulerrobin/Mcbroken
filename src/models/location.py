# location schema
from init import db, ma
from sqlalchemy import UniqueConstraint

class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), nullable = False)
    street = db.Column(db.String(100), nullable = False)
    postcode = db.Column(db.String(10), nullable = False)
    suburb = db.Column(db.String(100), nullable = False)
    state = db.Column(db.String(20), nullable = False)

    # Unique constraint for the combination of all columns
    __table_args__ = (
        UniqueConstraint('number', 'street', 'postcode', 'suburb', 'state', name='uq_location_details'),
    )


    # Do cascade deletes later for links
    reports = db.relationship('Report', back_populates='location', cascade='all, delete', lazy='dynamic') # lazy part allows for more control(filters)
    # Relates to report model in db

# Returning userSchema is only for admins unless searched username is same as user
class LocationSchema(ma.Schema):
    # Does not need to be linked to anything as it is linked as a DB for any future locations for reports

    class Meta:
        fields = ('id','number', 'street', 'postcode', 
        'suburb', 'state')