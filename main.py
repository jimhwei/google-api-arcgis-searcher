'''
google-api-json-writer
Scripted by Honglin (Jim) Wei
Date: 2021-11-24
'''
import os
import time
import json
import csv
import urllib.parse
from urllib.request import urlopen
from urllib.parse import quote
import arcpy
import pandas as pd

arcpy.env.overwriteOutput = True

# Replace the keys for your own!
geocode_key = 'AIzaSyAghqYiaSS2WiwxUjaFaJsoB16FejcGdxs'
nearby_key = 'AIzaSyBnui5g3BeTm3LcbBLBvbLrWFcwMEv6J8k'

query = input("What would you like to search?\nFor Example: Bubble Tea \n")
encoded_query = quote(query)

# Single Places only
def google_geocode():
    unparsed_place = input("Where would you like to have bubble tea? \n")
    place = urllib.parse.quote_plus(unparsed_place)
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={place}&key={geocode_key}"

    with urlopen(url) as response:
        source = response.read()

    data = json.loads(source)
    geocode_lat = (data['results'][0]['geometry']['location']['lat'])
    geocode_long = (data['results'][0]['geometry']['location']['lng'])
    
    return geocode_lat, geocode_long


def places_api_json_loader():
    
    # Default is 10000m search radius
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={places_lat}%2C{places_long}&radius=10000&keyword={encoded_query}tea&key={nearby_key}"

    with urlopen(url) as response:
        source = response.read()

    data = json.loads(source)
    return data

def csv_writer(data):
    
    # Writes the data into csv
    with open(r'.\bbt.csv', 'a+', newline='', encoding="utf-8") as f:
        file_path = r'.\bbt.csv' 
        fieldnames = ['places_id', 'name', 'lat', 'long', 'address', 'rating', 'price' ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        # check if size of file is 0 and inserts a header if necessary 
        if os.stat(file_path).st_size == 0:
            print('File is empty, inserting headers')
            writer.writeheader()

        # The heart of this project, loops through the individual api responses
        for num in range(len(data['results'])):
            place_id = data['results'][num]['place_id']
            name = data['results'][num]['name']
            lat = data['results'][num]['geometry']['location']['lat']
            long = data['results'][num]['geometry']['location']['lng']
            address = data['results'][num]['vicinity']
            rating = '' # Have to make an exception for price and ratings, since not all of them have prices
            price = ''
            
            try:
                rating = data['results'][num]['rating']
                price = data['results'][num]['price_level']
            except KeyError:
                pass
            
            # Writes the rows into the csv
            writer.writerow({'places_id': place_id, 'name': name, 'lat': lat, 'long': long, 'address': address, 'rating': rating, 'price': price})

def next_page(data):

    if data['next_page_token']:
        next_page_token = data['next_page_token']
    next_page_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={next_page_token}&key=AIzaSyBnui5g3BeTm3LcbBLBvbLrWFcwMEv6J8k"
    
    # Turns out the new token takes time to issue.. So we need to wait in between our calls
    # https://stackoverflow.com/questions/18724736/google-place-invalid-request-while-sending-request-to-get-next-page-results
    time.sleep(1.5)

    with urlopen(next_page_url) as response:
        source = response.read()

    next_page_data = json.loads(source)
    return next_page_data

# Cleans the duplicates in the csv using pandas
def remove_duplicates():

    file_name = "bbt.csv"
    file_name_output = "bbt.csv"

    df = pd.read_csv(file_name, engine='python', encoding="utf-8")

    # Notes:
    # - the `subset=None` means that every column is used 
    #    to determine if two rows are different; to change that specify
    #    the columns as an array
    # - the `inplace=True` means that the data structure is changed and
    #   the duplicate rows are gone  
    df.drop_duplicates(subset=None, inplace=True)

    # Write the results to a different file
    df.to_csv(file_name_output, index=False, encoding="utf-8")


#########################################################################

# Function driver

# Uses the polygon feature class at the following location
# Is there a way traverse directories instead of hard coding?
fc = r'C:\Users\jimwe\github\google-api-arcgis-integration\pro\YRBusinessDir2019\YRBusinessDir2019.gdb\GTAFSA_WGS84'

# Should be a way to get the geometry using the centroid, but using the shapexy gives non decimal degrees coordinates
cursor = arcpy.da.SearchCursor(fc, ['INSIDE_X', 'INSIDE_Y'])

# Loops through each FSA Polygon and assigns XY
# Calls and appends the function
call_count = 0
feature_count = 0

for row in cursor:
    places_lat, places_long = row[1], row[0]
    data = places_api_json_loader()
    csv_writer(data)
    call_count += 1
    feature_count += 1
    print(f"Processing feature {feature_count}")

    # If you really want to get all the next pages (Intensive!)
    # try: 
    # # We are assuming that the Google Maps returns a maximum of 60 responses over 3 pages
    #     new_data = next_page(data)
    #     csv_writer(new_data)
    #     call_count += 1

    #     new_data_2 = next_page(new_data)
    #     csv_writer(new_data_2)
    #     call_count += 1

    # except KeyError as err:
    #     pass

print(f"Google API was called {call_count} times")

# This uses ArcPy, which comes with an ArcGIS Pro installation
"""
# Converts CSV into an table called google_points.
arcpy.management.XYTableToPoint(r"C:\Users\jimwe\github\google-api-arcgis-integration\bbt.csv", r"C:\Users\jimwe\github\google-api-arcgis-integration\pro\YRBusinessDir2019\YRBusinessDir2019.gdb\google_points", "long", "lat", None, 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision')

# Deletes duplicate entries using places_id
arcpy.management.DeleteIdentical(r"C:\Users\jimwe\github\google-api-arcgis-integration\pro\YRBusinessDir2019\YRBusinessDir2019.gdb\google_points", "places_id", None, 0)
"""

print("The script is completed.")
