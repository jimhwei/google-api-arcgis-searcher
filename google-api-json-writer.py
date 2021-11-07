'''
Scripted by Honglin (Jim) Wei
All rights reserved
Date: 2021-11-16
google-api-json-writer v2
'''

import json
from urllib.request import urlopen

api_lat = input("Enter Latitude: ")
api_long = input("Enter Longitude: ")

def google_api_json_loader():
    
    with urlopen("https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=43.91407265468856%2C-79.44731313715351&radius=10000&keyword=bubbletea&key=AIzaSyBnui5g3BeTm3LcbBLBvbLrWFcwMEv6J8k") as response:
        source = response.read()

    data = json.loads(source)


def json_writer():

    result = []

    # Working with JSON
    # https://www.youtube.com/watch?v=9N6a-VLBa2I

    # Writes the data into json
    with open('bbt.json','w') as f:

        # Uses range and length of the list to create 
        # https://careerkarma.com/blog/python-typeerror-list-indices-must-be-integers-or-slices-not-str/
        for num in range(len(data['results'])):
            place_id = data['results'][num]['place_id']
            name = data['results'][num]['name']
            lat = data['results'][num]['geometry']['location']['lat']
            lng = data['results'][num]['geometry']['location']['lng']
            address = data['results'][num]['vicinity']

            # Converting the dictionaries back into a dictionary
            result.append({'name': name, 'lat': lat, 'lng': lng, 'place_id': place_id, 'address': address})
            
        json.dump(result, f)

# Write the data into csv
# with open('bbt.json','w') as f:
#     json.dump(data, f)