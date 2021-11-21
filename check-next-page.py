'''
Scripted by Honglin (Jim) Wei
All rights reserved
Date: 2021-11-16
google-api-json-writer v4.1
'''
import time
import json
from urllib.request import urlopen
import pandas as pd

key = 'AIzaSyBnui5g3BeTm3LcbBLBvbLrWFcwMEv6J8k'

def places_api_json_loader():
    
    # Default is 10000m search radius and searches bubble tea
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=43.6612785%2C-79.3868928&radius=10000&keyword=bubbletea&key={key}"

    with urlopen(url) as response:
        source = response.read()

    data = json.loads(source)
    return data

data = places_api_json_loader()

# print(data)

def next_page(data):

    if data['next_page_token']:
        next_page_token = data['next_page_token']
    next_page_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={next_page_token}&key=AIzaSyBnui5g3BeTm3LcbBLBvbLrWFcwMEv6J8k"
    
    # Turns out the new token takes time to issue.. So we need to sleep
    # https://stackoverflow.com/questions/18724736/google-place-invalid-request-while-sending-request-to-get-next-page-results
    time.sleep(1.5)

    with urlopen(next_page_url) as response:
        source = response.read()
        # print(source)

    next_page_data = json.loads(source)
    print("Next page ran")
    return next_page_data

# We are assuming that the Google Maps use 
new_data = next_page(data)
new_data_2 = next_page(new_data)

# print(data)
# print('\n'*3)
# print(new_data)

print("The script is completed.")