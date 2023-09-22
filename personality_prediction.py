import json
import requests
import pandas as pd

BASE_URL = "https://api.humantic.ai/v1/user-profile/create"
headers = {
    'Content-Type': 'application/json'
}
API_KEY = 'chrexec_4a27cd485a3c94289f2d82a51a4c2ea9'

df = pd.read_csv('transcripts.csv')
df['directorname'] = df['directorname'].str.lower()
df['directorname'] = df['directorname'].str.replace(' ', '_')
df = df.groupby('directorname')['string_agg'].sum().reset_index()
df.to_csv('personality_step_1.csv')

for index, row in df.iterrows():
    USER_ID = row['directorname']
    url = f"{BASE_URL}?apikey={API_KEY}&userid={USER_ID}"
    data = {'text': row['string_agg']}

    payload = json.dumps(data)
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.status_code, response.text)

    if index == 10:
        break