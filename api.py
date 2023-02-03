# The current version of the PatentsView API delivers data on patents granted through September 30, 2021.
# 55BfVeBf.wTgKzKmlZb3fjZhBlDtLllhqBcbE6TRH
# https://patentsview.org/apis/api-query-language

import requests
base_url = 'https://api.patentsview.org/patents/query?q='

def query_helper(query, value):
    return '{"' + str(query) + '":"' + str(value) + '"},'


def query(
    patent_number,
    inventor_last_name,
    patent_date,
):
    complete_query_str = ''

    if patent_number:
        complete_query_str += query_helper('patent_number', patent_number)

    if inventor_last_name:
        complete_query_str += query_helper('inventor_last_name', inventor_last_name)

    if patent_date:
        complete_query_str += query_helper('patent_date', patent_date)

    complete_query_str = complete_query_str[:-1]

    response = requests.get(base_url + '{"_and":[' + complete_query_str + ']}')
    print(response.text)

query(None, 'Whitney', '1981-10-06')