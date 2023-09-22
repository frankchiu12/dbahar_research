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

def get_reviews(api_key, business_id):
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    url = f'https://api.yelp.com/v3/businesses/{business_id}/reviews'
    response = requests.get(url, headers=headers)
    data = response.json()
    return data

api_key = os.getenv('API_KEY')
term = 'restaurants'
location = 'San Francisco, CA'

result_1 = search_businesses(api_key, term, location)
result_2 = get_reviews(api_key, 'KdH4w6BAc9ckVNZpyd4xWg')

with open('yelp_result_1.json', 'w') as file:
    json.dump(result_1, file, indent=4)
with open('yelp_result_2.json', 'w') as file:
    json.dump(result_2, file, indent=4)