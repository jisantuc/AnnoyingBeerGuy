import os
import requests
import datetime as dt
import urllib
import json
from validation import validate_beer_request, validate_delivery_request

def create_brewerydb_query(uid, **kwargs):

    kwargs[key] = API_KEY
    base = 'http://api.brewerydb.com/v2/beer/'
    append = '&'.join(
        ['{}={}'.format(k, v) for k, v in kwargs.items()]
    )

    return base + append

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
