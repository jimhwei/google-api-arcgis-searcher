'''
Scripted by Honglin (Jim) Wei
All rights reserved
Date: 2021-11-16
google-api-json-writer v4
'''

import json
import csv
import urllib.parse
from urllib.request import urlopen
import arcpy

fc = r'C:\Users\jimwe\github\google-api-arcgis-integration\pro\YRBusinessDir2019\YRBusinessDir2019.gdb\MarkhamRHFSA_WGS84'

# This function geocodes one point
def google_geocode():
    unparsed_place = input("Where would you like to have bubble tea? \n")
    place = urllib.parse.quote_plus(unparsed_place)
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={place}&key=AIzaSyAghqYiaSS2WiwxUjaFaJsoB16FejcGdxs"

    with urlopen(url) as response:
        source = response.read()

    data = json.loads(source)
    geocode_lat = (data['results'][0]['geometry']['location']['lat'])
    geocode_long = (data['results'][0]['geometry']['location']['lng'])
    
    # print(place, url, geocode_lat, geocode_long)
    return geocode_lat, geocode_long


def places_api_json_loader():
    
    # Default is 10000m search radius and searches bubble tea
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={places_lat}%2C{places_long}&radius=10000&keyword=bubbletea&key=AIzaSyBnui5g3BeTm3LcbBLBvbLrWFcwMEv6J8k"

    with urlopen(url) as response:
        source = response.read()

    data = json.loads(source)
    # print("places done")
    return data

places_lat, places_long = google_geocode()
data = places_api_json_loader()

def csv_writer():
    
    # Writes the data into json
    with open(r'.\bbt.csv', 'a+', newline='', encoding="utf-8") as f:
        fieldnames = ['places_id', 'name', 'lat', 'long', 'address', 'rating', 'price' ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for num in range(len(data['results'])):
            place_id = data['results'][num]['place_id']
            name = data['results'][num]['name']
            lat = data['results'][num]['geometry']['location']['lat']
            long = data['results'][num]['geometry']['location']['lng']
            address = data['results'][num]['vicinity']
            rating = data['results'][num]['rating']
            # For some reason i cannot access the price level?
            # Not all price level has 
            # if data['results'][num]['price_level']:
            #     print('yes')
            # else:
            #     print('null')
                
            writer.writerow({'places_id': place_id, 'name': name, 'lat': lat, 'long': long, 'address': address, 'rating': rating})
            print('places_id:', place_id, 'name:', name, 'lat:', lat, 'long: ', long, 'address:', address, 'rating:', rating)
        
# Driver Function
places_api_json_loader()
csv_writer()