from flask import request, redirect, render_template
from head import app, db
from backend.models import Clubevent, Studyroom, Meetup
# # import pandas as pd
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime, timedelta
# from config import MysqlConfig, sqliteConfig
from backend.club_info_scrapping import scrapping
from backend.utils import *


# app = Flask(__name__)


####### Test ######
@app.route("/")
def home():
    return "<p>Hello, Hello World!</p>"  # return test_func()

##################

# Create all tables
db.create_all()

# Create mock data
create_mock_studyroom()
create_mock_meetup()

# Scrape club events from web and store data to database
url = "https://umsu.unimelb.edu.au/things-to-do/events/"
scrapping(url)


@app.route('/clubevent', methods = ['GET'])
def get_club_events():
    # TODO: Parse user's filtering request
    # Filter by event_organisation, building name, date, start time, end time
    
    # Query the ClubEvent table in database
    club_events = Clubevent.query.order_by(Clubevent.content).all()
    
    # Push the filtered club events?
    return geojsonify(club_events)
    # return render_template("index.html", values = club_events)  # TODO: return a geojson


@app.route('/studyroom', methods = ['GET'])
def get_study_room():
    # TODO: Parse user's filtering request
    # Filter by e.g., Course, e.g., COMP - Computer Science, MAST - Maths, ENGR - Engineering
    # course name, building name, date, start time, end time
  
    # Query the ClubEvent table in database
    studyrooms = Studyroom.query.order_by(Studyroom.subject_id).all()
    
    # Push the filtered club events?
    return geojsonify(studyrooms)
    # return render_template("index.html", values = studyrooms)  # TODO: return a geojson


@app.route('/meetup', methods = ['POST', 'GET'])
def get_create_meetup():
    # Log user's request to create a meetup
    if request.method=='POST':
        # Parse user's request
        meetup_title = request.form['title']
        meetup_description = request.form['description']
        meetup_date = request.form['date']
        meetup_time_start = request.form['time_start']
        meetup_time_end = request.form['datetime_end']
        meetup_longitude = request.form['longitude']
        meetup_latitude = request.form['latitude']

        # Combine Date with time_start and time_end
        meetup_datetime_start = combine_date_time(meetup_date, meetup_time_start)  # TODO: what
        meetup_datetime_end = combine_date_time(meetup_date, meetup_time_end)

        # Create a row
        new_meetup = Meetup(content = meetup_title, 
                            description=meetup_description, 
                            datetime_start = meetup_datetime_start,
                            datetime_end = meetup_datetime_end, 
                            longitude = meetup_longitude,
                            latitude = meetup_latitude)
        
        try:
            # Store the log in session
            session['title'] = meetup_title
            session['description'] = meetup_description
            session['date'] = meetup_date
            session['time_start'] = meetup_time_start
            session['time_end'] = meetup_time_end
            session['longitude'] = meetup_longitude
            session['latitude'] = meetup_latitude
          
            # Store the new meetup to database
            db.session.add(new_meetup)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your meetup'
    
    else:
        # View all meetups
        meetups = Meetup.query.order_by(Meetup.datetime_start).all()
        return geojsonify(meetups)
        # return render_template("index.html", values = meetups)  # TODO: return a geojson

if __name__=='__main__':
    app.run(host = "localhost", port = 8001, debug = True)
