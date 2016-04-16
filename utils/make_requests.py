import os
import requests
import datetime as dt
import urllib
import json
from validation import validate_beer_request, validate_delivery_request

def create_brewerydb_query(request):
    validate_beer_request(request)

    base = 'http://api.brewerydb.com/v2/beers/'
    request.update({'key': os.environ['API_KEY']})
    response = requests.get(base, params=request).json()

    beer_names = []
    for data in response['data']:
        beer_names.append(data['name'])
    return beer_names

def make_delivery_request(request):
    base = (
        'https://delivery.com/api/data/search?search_type=alcohol'
        '&order_time=ASAP&order_type=delivery&client_id=brewhacks2016'
        '&section=beer'
    )

    req = request.args
    validate_delivery_request(req)
    resp = requests.get(
        base,
        {k: req[k] for k in ['address']} #more to add once available
    )

    if resp.status_code == 200:
        return resp.json()['data']['products']
    else:
        return 400

def filter_available_beers(available_beers, filter_to_names):
    return {'beers': [v for v in available_beers.itervalues() if
                      v['name'] in filter_to_names]}
