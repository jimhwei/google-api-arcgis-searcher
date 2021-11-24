import arcpy

fc = r'C:\Users\jimwe\github\google-api-arcgis-integration\pro\YRBusinessDir2019\YRBusinessDir2019.gdb\MarkhamRHFSA_WGS84'

# Should be a way to get the geometry using the centroid, but i don't remember how to right now
cursor = arcpy.da.SearchCursor(fc, ['x', 'y'])

# Loops through each FSA Polygon and assigns XY
for row in cursor:
    places_lat, places_long = row[1], row[0]