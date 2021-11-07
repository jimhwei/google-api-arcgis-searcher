'''
Scripted by Honglin (Jim) Wei
All rights reserved
Date: 2021-11-16
google-api-json-writer v2
'''

import json
from urllib.request import urlopen

def google_geocode():
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=Markham,Ontario&key=AIzaSyAghqYiaSS2WiwxUjaFaJsoB16FejcGdxs"

    with urlopen(url) as response:
        source = response.read()

    data = json.loads(source)
    geocode_lat = (data['results'][0]['geometry']['location']['lat'])
    geocode_long = (data['results'][0]['geometry']['location']['lng'])
    
    return geocode_lat, geocode_long

places_lat, places_long = google_geocode()


def places_api_json_loader():
    
    # Default is 10000m search radius and searches bubble tea
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={places_lat}%2C{places_long}&radius=10000&keyword=bubbletea&key=AIzaSyBnui5g3BeTm3LcbBLBvbLrWFcwMEv6J8k"

    with urlopen(url) as response:
        source = response.read()

    data = json.loads(source)
    return data

data = places_api_json_loader()

def csv_writer():

    result = []

    # Writes the data into json
    with open('bbt.csv','w') as f:

        for num in range(len(data['results'])):
            place_id = data['results'][num]['place_id']
            name = data['results'][num]['name']
            lat = data['results'][num]['geometry']['location']['lat']
            lng = data['results'][num]['geometry']['location']['lng']
            address = data['results'][num]['vicinity']

            # Converting the dictionaries back into a dictionary
            result.append({'name': name, 'lat': lat, 'lng': lng, 'place_id': place_id, 'address': address})
            
        json.dump(result, f)



google_geocode()
places_api_json_loader()
csv_writer()