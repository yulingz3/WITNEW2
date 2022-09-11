from head import db
from datetime import datetime


# Create schemas
class Clubevent(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)  # event name
    event_organisation = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Numeric(precision=14, scale=10),
                         default=-37.7986503)  # Set the default meetup place at South Lawn
    longitude = db.Column(db.Numeric(precision=14, scale=10),
                          default=144.9593367)  # Set the default meetup place at South Lawn

    # def __repr__(self):
    #     return '<Clubevent %r>' % self.id
    def __init__(self, content, event_organisation, duration, link, location, latitude, longitude):
        self.content = content
        self.event_organisation = event_organisation
        self.duration = duration
        self.link = link
        self.location = location
        self.latitude = latitude
        self.longitude = longitude


class Meetup(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    datetime_start = db.Column(db.DateTime, default=datetime.utcnow)  # the start of a meetup
    datetime_end = db.Column(db.DateTime, default=datetime.utcnow)  # the end of a meetup
    latitude = db.Column(db.Numeric(precision=14, scale=10),
                         default=-37.7986503)  # Set the default meetup place at South Lawn
    longitude = db.Column(db.Numeric(precision=14, scale=10),
                          default=144.9593367)  # Set the default meetup place at South Lawn

    def __init__(self, title, description, datetime_start, datetime_end, latitude, longitude):
        self.title = title
        self.description = description
        self.datetime_start = datetime_start
        self.datetime_end = datetime_end
        self.latitude = latitude
        self.longitude = longitude


class Studyroom(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)  # title
    subject_id = db.Column(db.String(9), nullable=False)
    room_no = db.Column(db.Integer)
    building_name = db.Column(db.String(200), nullable=False)
    datetime_start = db.Column(db.DateTime, default=datetime.utcnow)  # the start of a study room
    datetime_end = db.Column(db.DateTime, default=datetime.utcnow)  # the end of a study room
    latitude = db.Column(db.Numeric(precision=14, scale=10),
                         default=-37.7986503)  # Set the default meetup place at South Lawn
    longitude = db.Column(db.Numeric(precision=14, scale=10),
                          default=144.9593367)  # Set the default meetup place at South Lawn

    def __init__(self, content, subject_id, room_no, building_name, 
                 datetime_start, datetime_end, latitude, longitude):
        self.content = content
        self.subject_id = subject_id
        self.room_no = room_no
        self.building_name = building_name
        self.datetime_start = datetime_start
        self.datetime_end = datetime_end
        self.latitude = latitude
        self.longitude = longitude


