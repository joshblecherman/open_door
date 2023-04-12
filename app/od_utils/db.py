from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://postgres:opendoor@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Profiles(db.Model):
    __tablename__ = "profiles"
    
    user_id = db.Column(db.String(10), primary_key=True)
    dorm = db.Column(db.String(50))
    major = db.Column(db.String(50))
    description = db.Column(db.String(2000))

class Users(db.Model):
    __tablename__ = "users"
    
    user_id = db.Column(db.String(10), primary_key=True)
    dorm = db.Column(db.String(100), nullable=False)
    profile = db.Column(db.String(10),
                        db.ForeignKey("profiles.user_id"),
                        nullable = False)

class Activities(db.Model):
    __tablename__ = "activities"
    
    activity_id = db.Column(db.Uuid, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    place = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(2000))
    time = db.Column(db.DateTime, nullable=False)
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

class TicketmasterStaging(db.Model):
    __tablename__ = "ticketmaster_staging"
    
<<<<<<< HEAD
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    time = db.Column(db.DateTime, nullable=False)

def create_tables():
    with app.app_context():
        db.create_all()

def remove_all_tables():
    with app.app_context():
        Users.__table__.drop(db.engine)
        TicketmasterStaging.__table__.drop(db.engine)
        StudentEvents.__table__.drop(db.engine)
        Activities.__table__.drop(db.engine)
        Profiles.__table__.drop(db.engine)

def test_db():
    with app.app_context():
        create_tables()
        remove_all_tables()
        print(db.metadata.tables.__dir__())
=======
    fetch_statement = """
    SELECT * FROM users;
    """
    cur.execute(fetch_statement)
    records = cur.fetchall()
    print(records)
>>>>>>> origin/main

if __name__ == '__main__':
    test_db()