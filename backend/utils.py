from datetime import datetime
from backend.models import *
from geojson import Point, Feature, FeatureCollection

def create_mock_studyroom():
    '''Create mock data for study room'''
  
    studyroom = Studyroom('Cram everything for final exam', 'COMP10001', '156', 'Arts West',
                          datetime(2022, 9, 10, 16, 0), datetime(2022, 9, 10, 17, 0), 
                         -37.7976196,144.95722)
    db.session.add(studyroom)
    
    studyroom = Studyroom('Assignment 1', 'COMP10002', '155', 'Eastern Resource Centre',
                          datetime(2022, 9, 11, 16, 0), datetime(2022, 9, 11, 17, 0),
                         -37.7993769,144.9606714)
    db.session.add(studyroom)
    
    studyroom = Studyroom('Mid-term exam study group', 'COMP20008', '222', 'Law Library',
                          datetime(2022, 9, 12, 8, 0), datetime(2022, 9, 12, 11, 0),
                         -37.8029678,144.9577006)
    db.session.add(studyroom)
    
    db.session.commit()
    print("Mock study room data created ...")
    
    return None

def create_mock_meetup():
    '''Create mock data for meetup'''

    meetup = Meetup('Coffee meetup', "I'm the one in a blue hoodie", 
                    datetime(2022, 9, 11, 4, 0), datetime(2022, 9, 11, 4, 30), 
                    -37.7986136,144.9604578)
    
    db.session.add(meetup)
    
    meetup = Meetup('Lunch meetup', "I'm under the apple tree", 
                    datetime(2022, 9, 12, 12, 0), datetime(2022, 9, 12, 13, 30), 
                    -37.7983147,144.9601418)
    
    db.session.add(meetup)
    
    meetup = Meetup('Random meetup', "I'm wearing a red scarf", 
                    datetime(2022, 9, 13, 11, 0), datetime(2022, 9, 12, 12, 0), 
                    -37.7983147,144.9601418)  # TODO: please change it to a different location
    
    db.session.add(meetup)
    
    db.session.commit()
      
    print("Mock meetup data created ...")
    return None

def combine_date_time(date_obj, time_obj):
  '''Combine Date with Time. '''
  return datetime(date_obj.year, date_obj.month, date_obj.day, 
           time_obj.hour, time_obj.minute)

def geojsonify(table):
   ''' Return SQLAlchemy rows with latitude and longitude
   as a dictionary in GeoJson format'''

   features = []
   for item in table:
        # TODO filter null lat or lng
      # try:
      point = Point((item.longitude, item.latitude))
      # except:
      #   continue
      properties = dict(item.__dict__)  # Convert the current row to dictionary
    
    #   properties = {'whatever':"whatever"}
    
      # Remove unnecessay items
      properties.pop("_sa_instance_state")
    #   properties.pop("latitude")
      
      features.append(Feature(geometry = point,
                              properties = properties
                              )
                      )
       
   feature_collection = FeatureCollection(features)
   return feature_collection
  