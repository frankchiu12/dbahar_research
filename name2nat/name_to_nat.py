import pandas as pd
import requests

# https://bookdown.org/paul/apis_for_social_scientists/genderize.io-api.html
# https://www.askpython.com/python/examples/predict-nationality-using-names
# GNR

df = pd.read_csv('name2nat/inventornames_10k_sample.csv')
df['full_name'] = df['inventor_first_name'] + ' ' + df['inventor_last_name']
name_list = df['full_name'].tolist()

for i, name in enumerate(name_list):
    response = requests.get('https://api.nationalize.io?name=' + name)
    if response.status_code == 200:
        data = response.json()
        print(data)    
    if i == 10:
        break

url_origin = "https://v2.namsor.com/NamSorAPIv2/api2/json/originBatch"
url_country = "https://v2.namsor.com/NamSorAPIv2/api2/json/countryBatch"

for i, name in enumerate(name_list):
    # origin
    payload = {
    "personalNames": [
        {
        "id": "e630dda5-13b3-42c5-8f1d-648aa8a21c42",
        "firstName": name.partition(' ')[0],
        "lastName": name.partition(' ')[2]
        }
    ]
    }
    headers = {
        "X-API-KEY": "a3f236da0acbac71b4adae61fc69a57e",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url_origin, json=payload, headers=headers).json()
    response = response['personalNames'][0]
    print(name, response['countryOrigin'], response['countryOriginAlt'], response['probabilityCalibrated'], response['probabilityAltCalibrated'])

    # residence
    payload = {
    "personalNames": [
        {
        "id": "9a3283bd-4efb-4b7b-906c-e3f3c03ea6a4",
        "firstName": name.partition(' ')[0],
        "lastName": name.partition(' ')[2]
        }
    ]
    }
    headers = {
        "X-API-KEY": "a3f236da0acbac71b4adae61fc69a57e",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url_origin, json=payload, headers=headers)
    print(response.text)

    if i == 10:
        break