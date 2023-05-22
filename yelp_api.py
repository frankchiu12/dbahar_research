# https://docs.developer.yelp.com/reference/v3_business_search

import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
API_KEY = os.getenv('API_KEY')

def search_businesses(api_key, term, location):
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    url = "https://api.yelp.com/v3/businesses/search"
    params = {
        "term": term,
        "location": location
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    return data

api_key = os.getenv('API_KEY')
term = 'restaurants'
location = 'San Francisco, CA'

result = search_businesses(api_key, term, location)
with open('yelp_result.json', 'w') as file:
    json.dump(result, file, indent=4)