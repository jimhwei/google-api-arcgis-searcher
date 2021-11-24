import arcpy
# fc = r"C:\Users\jimwe\github\google-api-arcgis-integration\pro\YRBusinessDir2019\YRBusinessDir2019.gdb\GTAFSA_WGS84"
# cursor = arcpy.da.SearchCursor(fc, ["SHAPE@XY"])
# polygons = 0

# for row in cursor:
#     print(row[0])
#     polygons += 1

# print (polygons)

fc = r'C:\Users\jimwe\github\google-api-arcgis-integration\pro\YRBusinessDir2019\YRBusinessDir2019.gdb\GTAFSA_WGS84'

# Should be a way to get the geometry using the centroid, but i don't remember how to right now
cursor = arcpy.da.SearchCursor(fc, ['INSIDE_X', 'INSIDE_Y'])

# Loops through each FSA Polygon and assigns XY
# Calls and appends the function
for row in cursor:
    places_lat, places_long = row[1], row[0]
    print(places_lat, places_long)