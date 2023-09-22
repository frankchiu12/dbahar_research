import requests
import pandas as pd

BASE_URL = "https://api.humantic.ai/v1/user-profile"
headers = {
    'Content-Type': 'application/json'
}
API_KEY = 'chrexec_4a27cd485a3c94289f2d82a51a4c2ea9'

df = pd.read_csv('personality_step_1.csv')

for index, row in df.iterrows():
    USER_ID = row['directorname']
    url = f"{BASE_URL}?apikey={API_KEY}&id={USER_ID}"
    response = requests.request("GET", url, headers=headers)

    o = response.json()['results']['personality_analysis']['ocean_assessment']['openness']['score']
    c = response.json()['results']['personality_analysis']['ocean_assessment']['conscientiousness']['score']
    e = response.json()['results']['personality_analysis']['ocean_assessment']['extraversion']['score']
    a = response.json()['results']['personality_analysis']['ocean_assessment']['agreeableness']['score']
    n = response.json()['results']['personality_analysis']['ocean_assessment']['emotional_stability']['score']

    print(o, c, e, a, n)

    if index == 10:
        break