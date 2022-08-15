from dataclasses import replace
from requests_html import HTMLSession
import json
import re


oldword = input('Enter old word: ')
new_word = input('Enter new word: ')
asin = input('Enter ASIN: ')
with open(asin + '-reviews.json', 'r+') as f:
    data = json.load(f)
for item in data:
    replaces = {}
    replaces[oldword] = new_word 
    item['body'] = re.sub("|".join(replaces.keys()), lambda match: replaces[match.string[match.start():match.end()]], item['body'])
with open(asin + '-reviews.json', 'w') as f:
    json.dump(data, f)
