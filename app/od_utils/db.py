from flask_sqlalchemy import SQLAlchemy
from flask import Flask, current_app
import uuid

app = current_app
db = SQLAlchemy()

class Profiles(db.Model):
    __tablename__ = "profiles"
    
    net_id = db.Column(db.String(10), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    preferred_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    dorm = db.Column(db.String(50))
    major = db.Column(db.String(50))
    description = db.Column(db.String(2000))

class Users(db.Model):
    __tablename__ = "users"
    
    net_id = db.Column(db.String(10), primary_key=True)
    dorm = db.Column(db.String(100), nullable=False)
    profile = db.Column(db.String(10),
                        db.ForeignKey("profiles.net_id"),
                        nullable = False)

class Activities(db.Model):
    __tablename__ = "activities"
    
    activity_id = db.Column(db.Uuid, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    place = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(2000))
    datetime = db.Column(db.DateTime, nullable=False)
    fee = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(255))
    img = db.Column(db.LargeBinary)
    reservation_needed = db.Column(db.Boolean, nullable=False)
    rsvp_list = db.Column(db.ARRAY(db.String(10)))

class StudentEvents(db.Model):
    __tablename__ = "student_events"
    
    id = db.Column(db.Uuid,
                   db.ForeignKey("activities.activity_id"),
                   primary_key=True)
    notes = db.Column(db.String(2000))

class Ticketmaster(db.Model):
    __tablename__ = "ticketmaster"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    img_url = db.Column(db.String(255))
    url = db.Column(db.String(255), nullable=False)

# Ignores any conflicts with existing tables.
# Bear in mind any tables with the same name will not be made.
# Any table structure changes must be done via the database's CLI.
# Alternatively, drop all tables and recreate them.
def create_tables():
    with app.app_context():
        db.create_all()

# USE SPARINGLY DO NOT EVER USE THIS IN PRODUCTION
# (So why did I make this? I dunno...)
def drop_all_tables():
    tables = [Users, Ticketmaster, StudentEvents, Activities, Profiles]

    with app.app_context():
        inspect = db.inspect(db.engine)
        for table in tables:
            if inspect.has_table(table.__tablename__):
                table.__table__.drop(db.engine)

def test_db():
    with app.app_context():
        create_tables()

# Just for testing
# if __name__ == '__main__':
#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = \
#         'postgresql://postgres:opendoor@localhost:5432/postgres'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     db.init_app(app)
#     test_db()