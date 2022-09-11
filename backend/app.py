# This script is the entry & exit point to our app

from flask import Flask, request, redirect, render_template, jsonify
# import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from config import MysqlConfig, sqliteConfig
from flask_cors import CORS
# from flask_marshmallow import Marshmallow

app = Flask(__name__)
CORS(app)

# Test
@app.route("/")
def home():
    return render_template("index.html")


# Connect to database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

app.secret_key = "abc"
app.config.from_object(MysqlConfig)
app.permanent_session_lifetime = timedelta(minutes=1)
db = SQLAlchemy(app)
# ma = Marshmallow(app)


# Create schema(s)
# Will move this bit to models.py later
class Meetup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    datetime_start = db.Column(db.DateTime, default=datetime.utcnow)  # the start of a meetup
    datetime_end = db.Column(db.DateTime, default=datetime.utcnow)  # the end of a meetup

    def __repr__(self):
        return '<Meetup %r>' % self.id


# Create schema(s)
# Will move this bit to models.py later
class Studyroom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_no = db.Column(db.Integer)
    building_id = db.Column(db.Integer)
    datetime_start = db.Column(db.DateTime, default=datetime.utcnow)  # the start of a study room
    datetime_end = db.Column(db.DateTime, default=datetime.utcnow)  # the end of a study room

    def __repr__(self):
        return '<Study room %r>' % self.id

#class MeetupSchema(ma.Schema):
#    class Meta:
#        fields = ('id', 'content', 'body', 'date')

# meetup_schema = MeetupSchema()
# meetups_schema = MeetupSchema(many=True) 

# @app.route('/clubevents', methods=['GET'])
# def get_club_events():
#   # Parse user's filtering request?

#   # Query the ClubEvent table in database?
#   club_events = pd.read_csv("club_events.csv")

#   # Push the filtered club events?
#   return club_events


# @app.route('/studyroom', methods=['GET'])
# def get_study_room():
#   return None  # return study_room_filtered


@app.route('/meetup', methods=['POST', 'GET'])
def create_meetup():
    # Log user's request to create a meetup
    if request.method == 'POST':

        # Parse user's request
        meetup_content = request.form['content']
        meetup_datetime_start = request.form['datetime_start']
        meetup_datetime_end = request.form['datetime_end']
        meetup_longitude = request.form['longitude']
        meetup_latitude = request.form['latitude']

        new_meetup = Meetup(content=meetup_content, datetime_start=meetup_datetime_start,
                            datetime_end=meetup_datetime_end, longitude = meetup_longitude, latitude = meetup_latitude)

        try:
            # Store the new meetup to database
            db.session.add(new_meetup)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your meetup'

    else:
        # View all meetups
        meetups = Meetup.query.order_by(Meetup.datetime_start).all()
        #results = meetups_schema.dump(meetups)
        #return jsonify(results)
        #return meetup_schema.jsonify(results)
        return render_template("index.html", values=meetups)  # TODO: link the output with React


# if __name__ == "__main__":
#     app.run()  # debug=True)

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
