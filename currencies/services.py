import os
import requests


def request_updated_rates(default_currency, currencies):
    url = 'http://apilayer.net/api/live'
    params = {
        'access_key': os.environ.get('CURR_LAYER_ACCESS_KEY'),
        'currencies': currencies,
        'source': default_currency,
        'format': 1
    }
    response = requests.get(url, params=params)
    return response.json()['quotes']

