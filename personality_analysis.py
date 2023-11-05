import requests
import pandas as pd
import time

BASE_URL = "https://api.humantic.ai/v1/user-profile"
headers = {
    'Content-Type': 'application/json'
}
API_KEY = 'chrexec_4a27cd485a3c94289f2d82a51a4c2ea9'

df = pd.read_csv('personality_step_1.csv')
res_df = pd.DataFrame()

CEO_list = []
o_list = []
c_list = []
e_list = []
a_list = []
n_list = []

for index, row in df.iterrows():
    try:
        if index < 49:
            continue
        if index % 20 == 0:
            time.sleep(300)
        USER_ID = row['directorname']
        url = f"{BASE_URL}?apikey={API_KEY}&id={USER_ID}"
        response = requests.request("GET", url, headers=headers)
        print(response.json())

        o = response.json()['results']['personality_analysis']['ocean_assessment']['openness']['score']
        c = response.json()['results']['personality_analysis']['ocean_assessment']['conscientiousness']['score']
        e = response.json()['results']['personality_analysis']['ocean_assessment']['extraversion']['score']
        a = response.json()['results']['personality_analysis']['ocean_assessment']['agreeableness']['score']
        n = response.json()['results']['personality_analysis']['ocean_assessment']['emotional_stability']['score']

        CEO_list.append(USER_ID)
        o_list.append(o)
        c_list.append(c)
        e_list.append(e)
        a_list.append(a)
        n_list.append(n)

    except:
        break

res_df['CEO'] = CEO_list
res_df['openness'] = o_list
res_df['conscientiousness'] = c_list
res_df['extraversion'] = e_list
res_df['agreeableness'] = a_list
res_df['emotional_stability'] = n_list

res_df.to_csv('personality_step_2.csv')