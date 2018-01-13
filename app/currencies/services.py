import requests

def request_updated_rates():
    url = 'http://apilayer.net/api/live'
    params = {
        'access_key': '31fbc24c4aca6f7a9a6c2ae83a1a304b',
        'currencies': 'EUR,BRL,BTC',
        'source': 'USD',
        'format': 1
    }
    response = requests.get(url, params=params)
    return response.json()['quotes']

