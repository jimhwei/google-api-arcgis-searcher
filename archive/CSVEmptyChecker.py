import csv

# with open(r'.\bbttest.csv', 'a+', newline='', encoding="utf-8") as f:
#         fieldnames = ['places_id', 'name', 'lat', 'long', 'address', 'rating', 'price' ]
#         writer = csv.DictWriter(f, fieldnames=fieldnames)
#         # writer.writeheader()
        
#         csvreader = csv.reader(f)
#         for row in csvreader:
#             print(row)
#             if not row[0]:
#                 print("12")

# with open('bbttest.csv', 'rb') as csvfile:
#     sniffer = csv.Sniffer()
#     has_header = sniffer.has_header(csvfile.read(2048))
#     csvfile.seek(0)

# import pandas as pd

# df = pd.read_csv(r'bbttest.csv') # or pd.read_excel(filename) for xls file
# df.empty # will return True if the dataframe is empty or False if not.

# if df.empty is True:
#     print("Do something")

import os
file_path = 'bbttest.csv'
# check if size of file is 0
if os.stat(file_path).st_size == 0:
    print('File is empty')
else:
    print('File is not empty')