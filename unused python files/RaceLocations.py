import pandas as pd
import math
from datetime import date
import urllib.request
import json

from timezonefinder import TimezoneFinder
import datetime
import pytz

datetime.datetime.now(pytz.timezone('Asia/Jerusalem')).strftime('%z')

# returns '+0300' (because 'now' they have DST)


pytz.timezone('Asia/Jerusalem').localize(datetime.datetime(2011,1,1)).strftime('%z')

# returns '+0200' (because in January they didn't have DST)

weather_api_key = '69UKZ9EEPFKZCPURUQN84IRJ7'
weather_api_endpoint = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history'

races = pd.read_csv(r'F1_data\races.csv')
circuits = pd.read_csv(r'F1_data\circuits.csv')

tf = TimezoneFinder()
circuits['timezone'] = circuits.apply(lambda x: tf.timezone_at(lng=x['lng'], lat=x['lat']), axis=1)

# merge race date with circuit location details:
race_loc = races[['raceId', 'circuitId', 'date', 'time']].merge(
    circuits[['circuitId', 'location', 'country', 'lat', 'lng', 'timezone']],
    on='circuitId')

race_loc.loc[race_loc.time == r"\N"] = "12:00:00"

race_loc['date'] = pd.to_datetime(race_loc.date)
#race_loc = race_loc.sort_values('date', ascending=False)
race_loc = race_loc[race_loc.date < date.today()]
race_loc.reset_index(drop=True, inplace=True)

race_loc['timezone_hours'] = race_loc.apply(lambda x: pytz.timezone(x['timezone']).localize(x['date']).strftime('%z'), axis=1)
race_loc['date_time'] = pd.to_datetime(race_loc['time'], errors='coerce', format='%H:%M:%S')
race_loc['local_time'] = race_loc.apply(lambda x: x['time'].datetime.replace(tzinfo=pytz.timezone(x['timezone']).localize(x['date'])), axis=1)

d.replace(tzinfo=tz)
records = []
labels = ['raceId', 'date', 'lat', 'lng', 'temp', 'precip', 'wspd', 'visibility', 'conditions']
for i, row in race_loc.iterrows():

    raceId = row['raceId']
    date = row['date']
    time = row['time']
    latitude = row['lat']
    longitude = row['lng']

    if math.isnan(latitude) or math.isnan(longitude) or (latitude == 0 and longitude == 0):
        print("Bad latlon {},{}".format(latitude, longitude))
        continue

    latitude = '{:.5f}'.format(latitude)
    longitude = '{:.5f}'.format(longitude)

    query_params = '&contentType=json&aggregateHours=24&unitGroup=metric&key={}&startDateTime={}&endDateTime={' \
                   '}&locations={},{} '

    query_params = query_params.format(weather_api_key, date.isoformat(), date.isoformat(), latitude, longitude)

    try:
        response = urllib.request.urlopen(weather_api_endpoint
                                          + "?" + query_params)
        data = response.read()
    except Exception:
        print("Error reading from {}"
              .format(weather_api_endpoint + "?" + query_params))
        continue

    weatherData = json.loads(data.decode('utf-8'))

    errorCode = weatherData["errorCode"] if 'errorCode' in weatherData else 0

    if (errorCode > 0):
        print("Error reading from errorCode {}, error={}"
              .format(weather_api_endpoint +
                      "?" + query_params, errorCode))
        continue

    locations = weatherData["locations"]
    for locationid in locations:
        location = locations[locationid]
        for value in location["values"]:
            records.append((raceId, date.isoformat(), latitude, longitude, value["temp"],
                            value["precip"], value["wspd"], value['visibility'], value['conditions']))

output_df2 = pd.DataFrame.from_records(records, columns=labels)
output_df2.to_csv('output.csv', index=False)
