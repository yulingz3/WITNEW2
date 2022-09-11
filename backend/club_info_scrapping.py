import pandas as pd
import requests
from bs4 import BeautifulSoup
# import re
from backend.models import Clubevent
from head import db
# from datetime import datetime
import geocoder


def scrapping(url):
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")

    a = []
    for result in soup.find_all("span", {"class": "msl_event_organisation"}):  # event organization
        a.append(result.text.strip())
    b = []
    for result in soup.find_all("dd", {"class": "msl_event_time"}):  # date-time
        b.append(result.text.strip())
    c = []
    num = 0
    for result in soup.find("div", {"class": "msl_eventlist"}).find_all('a'):  # event link
        href = result['href']
        if not href.startswith('/ents/eventlist/') and num % 2 == 0:
            if href.startswith('/events'):
                href = "https://umsu.unimelb.edu.au" + href
            c.append(href)
        num += 1
    d = []
    for result in soup.find_all("dd", {"class": "msl_event_location"}):  # location
        d.append(result.text.strip())

    names = []
    for result in soup.find_all("a", {"class": "msl_event_name"}):  # date-time
        names.append(result.text.strip())

    lat = [-37.79674, -37.79856, -37.80126]
    long = [144.96084, 144.96032, 144.96114]
# union house: -37.79674, 144.96084; south lawn -37.79856, 144.96032; giblin: -37.80126, 144.96114
    dict1 = {'Event organization': a[:3], 'Date-time': b[:3], 'Link': c[:3], 'Location': d[:3], 'Event name': names[:3], 'Latitude': lat, 'Longitude':long}
    df = pd.DataFrame(dict1)

    #df_log_lat = pd.DataFrame({'Latitude': lat, 'Longitude':long})
    #pd.merge(df, df_log_lat, how = "left_on")

    # df_processed = df[(df['Location'] != "Online") & (df['Location'] != "Zoom") & (df['Location'].notna()) & (df['Location'] != 'https://forms.office.com/r/PJWSPhcRBC')]
    # df_processed = df_processed[~df_processed['Location'].isin(['http'])]
    # df_processed.Location = df_processed.Location.apply(lambda x: 'Online' if 'http' in x else x)
    # df_processed = df_processed[(df_processed['Location'] != "Online")]
    # df_processed.Location = df_processed.Location.apply(lambda x: 'Union House' if 'Union House' in x else x)
    
    # lng = []
    # lat = []
    # for loc in df_processed['Location']:
    #     g = geocoder.bing(loc, key=api_key)
    #     results = g.json
    #     lat.append(results['lat'])
    #     lng.append(results['lng'])
    # df_processed['Latitude'] = lat
    # df_processed['Longitude'] = lng

    # Clear the table before adding scraped rows
    Clubevent.query.delete()  
    
    # Insert each club event to table "Clubevent"
    for index, row in df.iterrows():
        event = Clubevent(row['Event name'], row['Event organization'], row['Date-time'], row['Link'], row['Location'], row['Latitude'], row['Longitude'])
        db.session.add(event)
    db.session.commit()
    
    return None

# url = "https://umsu.unimelb.edu.au/things-to-do/events/"
# df = scrapping(url)
