import os
import requests
import datetime as dt
import urllib
import json
from validation import validate_beer_request, validate_delivery_request

def create_brewerydb_query(request):
    req = dict(request.values.items())
    validate_beer_request(req)
    base = 'http://api.brewerydb.com/v2/beers'
    req.update({'key': os.environ['API_KEY']})
    response = requests.get(base, params=req).json()
    with open('breweryresponse.txt', 'w') as outf:
        outf.write(json.dumps(response))

    beer_names = [
        d['name'] for d in response['data']
    ] if 'data' in response else []

    return beer_names

def make_delivery_request(request):
    base = (
        'https://delivery.com/api/data/search?search_type=alcohol'
        '&order_time=ASAP&order_type=delivery&client_id=brewhacks2016'
        '&section=beer'
    )

    req = dict(request.values.items())
    if req['address'] == 'New York, NY':
        req['address'] = '1129 E 14th St, New York, NY'
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
    return {'beers': [
        v for v in available_beers.itervalues() if
        any([f.lower() in v['name'].lower()
             for f in filter_to_names])
    ]}
