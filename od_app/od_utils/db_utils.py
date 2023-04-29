"""Utility module for reading from and modifying database.

Note: When SQLAlchemy class (Type[db.Model]) is referred to as a type,
it refers to a class name such as Profiles or Users.
When SQLAlchemy object (db.Model) is referred to as a type,
it refers to an object pertaining to a class,
such as Profiles(net_id="jd1234", first_name="John", last_name="Doe")
"""

from flask import Flask
from typing import Type

import datetime
import hashlib
import jwt
import uuid

from od_app import db
from od_app import app

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
    password = db.Column(db.String(100), nullable=False)
    profile = db.Column(db.String(10),
                        db.ForeignKey("profiles.net_id"),
                        nullable = False)

    # Code stolen from
    # https://github.com/realpython/flask-jwt-auth/blob/d252dd88c7271580cbebc24c54f0259779123537/project/server/models.py#L28
    def encode_auth_token(self, net_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': net_id
            }
            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

class Activities(db.Model):
    __tablename__ = "activities"
    
    activity_id = db.Column(db.Uuid, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    place = db.Column(db.String(255))
    description = db.Column(db.String(5000))
    datetime = db.Column(db.DateTime, nullable=False)
    fee = db.Column(db.Integer)
    url = db.Column(db.String(255))
    img_url = db.Column(db.String(255))
    reservation_needed = db.Column(db.Boolean, nullable=False)
    source = db.Column(db.String(63), nullable=False)
    rsvp_list = db.Column(db.ARRAY(db.String(10)))

class NYUEvents(db.Model):
    __tablename__ = "nyu_events"
    id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(255))
    url = db.Column(db.String(255))
    date_time = db.Column(db.DateTime)
    img_url = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(5000), nullable=True)
    fee = db.Column(db.Integer, nullable=True)

class Ticketmaster(db.Model):
    __tablename__ = "ticketmaster"

    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    img_url = db.Column(db.String(255))
    url = db.Column(db.String(255), nullable=False)

class StudentEvents(db.Model):
    __tablename__ = "student_events"
    
    net_id = db.Column(db.String(10), primary_key = True)
    title = db.Column(db.String(255), nullable = False)
    place = db.Column(db.String(127), nullable = False)
    description = db.Column(db.String(2000))
    fee = db.Column(db.Integer)
    url = db.Column(db.String(255))
    date = db.Column(db.Date, nullable = False)
    time = db.Column(db.Time, nullable = False)
    reservation_needed = db.Column(db.Boolean, nullable = False)
    
    def add_to_activities(self):
        attr = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        date = attr['date']
        time = attr['time']
        net_id = attr['net_id']
        attr.pop('date')
        attr.pop('time')
        attr.pop('net_id')
        
        attr['source'] = "student_events"
        attr['datetime'] = date + " " + time
        curr_time = datetime.datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        hash_str = net_id + attr['title'] + attr['place'] + \
                    date + time + curr_time
        hash_md5 = hashlib.md5(bytes(hash_str, 'utf-8')).hexdigest()
        attr['activity_id'] = uuid.UUID(hash_md5)
        
        add(Activities(**attr))


class Spots(db.Model):
    __tablename__ = "spots"
    spot_id = db.Column(db.Uuid, primary_key=True)
    name = db.Column(db.String(127), nullable=False)
    place = db.Column(db.String(127), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    source = db.Column(db.String(63))


class ParkTrails(db.Model):
    __tablename__ = "park_trails"
    trail_id = db.Column(db.Uuid, primary_key=True, nullable=False)
    trail_name = db.Column(db.String(127), nullable=False)
    park_name = db.Column(db.String(127), nullable=False)
    surface = db.Column(db.String(127), nullable=True)
    topography = db.Column(db.String(127), nullable=True)
    difficulty = db.Column(db.String(127), nullable=True)
        
def create_tables():
    """Ignores any conflicts with existing tables.
    Bear in mind any tables with the same name will not be made.
    Any table structure changes must be done via the database's CLI.
    Alternatively, drop all tables and recreate them.
    
    return: None
    """
    with app.app_context():
        db.create_all()

def drop_all_tables():
    """USE THIS SPARINGLY NEVER USE THIS IN PRODUCTION
    (So why did I make this? I dunno...)
    
    return: None
    """
    tables = [Spots, ParkTrails]

    with app.app_context():
        inspect = db.inspect(db.engine)
        for table in tables:
            if inspect.has_table(table.__tablename__):
                table.__table__.drop(db.engine)
        db.session.commit()

def add(data: db.Model, commit=True, overwrite=False):
    """Inserts model into its respective table.
    
    :param data: SQLAlchemy object to be inserted
    :param commit: Pushes changes immediately to database if True.
    :param overwrite: If True, overwrite existing
    data if primary key is found in table
    
    :return: None
    """
    with app.app_context():
        if overwrite:
            db.session.merge(data)
        else:
            db.session.add(data)

        if commit:
            db.session.commit()

def get_with_pk(table_class: Type[db.Model], pk: any) -> db.Model:
    """Retrieves the single model corresponding to the primary key.
    
    :param table_class: SQLAlchemy class to get data from
    :param pk: Primary key used to find desired row.
    
    :return: SQLAlchemy model if found, None otherwise."""
    with app.app_context():
        return db.session.get(table_class, pk)

def get_with_attributes(table_class: Type[db.Model], attr = {}) -> db.Model:
    """Retrieves the models matching the corresponding attributes.
    
    :param table_class: SQLAlchemy class to get data from
    :param attr: Dictionary of filters to use.
    Empty dict returns the whole table.
    
    e.g. Passing in (Users, {"first_name":"John", "last_name":"Doe"})
    generates the SQL statement
    
    select *
    in users
    where first_name = 'John'
    and last_name = 'Doe'
    
    :return: List of all SQLAlchemy objects matching the filter."""
    with app.app_context():
        return table_class.query.filter_by(**attr).all()

def get_col_names(table_class: Type[db.Model]) -> list[str]:
    """Retrieves column names for a table.
    
    :param table_class: SQLAlchemy class to get data from
    
    :return: List of column names."""
    with app.app_context():
        return table_class.__table__.columns.keys()

def login(net_id, pw):
    """Logs in a user with the requested username and password.
    
    :param net_id: NYU NetID used to login
    :type net_id: str
    :param pw: User password
    :type pw: pw
    
    :return: Token on successful authentication, None otherwise
    """
    user = get_with_attributes(Users, {"net_id": net_id, "password": pw})
    if user != None:
        return user[0].encode_auth_token(net_id)
    
    return None

def delete(table_class: Type[db.Model], pk: any, commit = True) -> db.Model:
    """Deletes model from its respective table via its primary key.
    
    :param table_class: SQLAlchemy class to get data from
    :param pk: Primary key used to find desired row.
    :param commit: Pushes changes immediately to database if True.
    
    :return: Deleted SQLAlchemy model if found, None otherwise
    """
    data = get_with_pk(table_class, pk)
    with app.app_context():
        if data != None:
            db.session.delete(data)

        if commit:
            db.session.commit()

    return data

def run_raw_sql(statement: str, get_output: bool=False):
    """Runs the given SQL statement. Use as sparingly as possible,
    as this does not work with the SQLAlchemy models, but rather
    returns lists of tuples. No error checking is done here,
    and inputs are not sanitized (yet?), so run at your own risk.
    
    :param statement: SQL statement to run.
    :param get_output: True if the output should be returned.
    If the query does not return rows, setting get_output=True will raise an exception
    :type statement: str
    
    :return: List of results of SQL statement if get_output is True
    """
    res = None
    with app.app_context():
        if get_output:
            res = db.session.execute(db.text(statement)).all()
            db.session.commit()
        else:
            db.session.execute(db.text(statement))
            db.session.commit()
            db.session.close()
    return res


def commit():
    """Saves all changes to the database.
    
    :return: None
    """
    with app.app_context():
        db.session.commit()

def test_db():
    with app.app_context():
        # drop_all_tables()
        create_tables()
        for i in range(1, 10):
            p = Profiles(**{"net_id": "asdf" + str(i),
                        "first_name": "first" + str(i),
                        "last_name": "last" + str(i)})
            u = Users(**{"net_id": "asdf" + str(i),
                    "password": "pw" + str(i),
                    "profile": p.net_id})
            add(p, overwrite=True)
            add(u, overwrite=True)

    # print(get_with_attribute(Users, {"net_id":"asdf1", "password":"pw1"}))
    # print(get_with_pk(Users, "asdf1"))
    # print(type(get_with_pk(Users, "asdf1")))
    
    # print(delete(Users, "asdf1"))
    # print(get_with_attribute(Users, {"net_id":"asdf1", "password":"pw1"}))
    # print(get_with_pk(Users, "asdf1"))
    # print(get_with_attribute(Users))
    # print(Users.__dict__)
    
    # user = get_with_pk(Users, "asdf1")
    # cols = get_col_names(Users)
    # for col in cols:
    #     print(type(user.__dict__))
    # run_raw_sql("select * from users")
    
    # login("asdf2", "pw2")

# Just for testing
if __name__ == '__main__':
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgresql://postgres:opendoor@localhost:5432/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "wzb9Sp@WCn!3t4Jy" #For login tokens
    db.init_app(app)
    
    test_db()