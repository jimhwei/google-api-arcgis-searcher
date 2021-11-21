from urllib.parse import quote

query = "Think and wonder, wonder and think."

encoded_query = quote(query)


print(encoded_query)