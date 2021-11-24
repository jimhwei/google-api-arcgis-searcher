import pandas as pd
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