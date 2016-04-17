import os
import requests
import datetime as dt
import urllib
import json
from fuzzywuzzy import fuzz
from validation import validate_beer_request, validate_delivery_request

def create_brewerydb_query(request):
    req = dict(request.values.items())
    validate_beer_request(req)
    base = 'http://api.brewerydb.com/v2/beers'
    req.update({'key': os.environ['API_KEY'],
                'order': 'random'})

    response = requests.get(base, params=req).json()
    data = response['data']
    if response['numberOfPages'] > 1:
        for p in range(2, min(10, response['numberofPages']) + 1):
            req.update({'p': p})
            data += requests.get(base, req).json()['data']

    beer_names = [
        {'name': d['name'],
         'abv': d['abv'],
         'ibu': d['ibu'],
         'brewer': ' '.join([b['name'] for b in d['breweries']])} for d in data
    ] if 'data' in response else []
    for bn in beer_names:
        bn['longname'] = ' '.join([bn['brewer'], bn['name']])

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

    data = resp.json()['data']['products'].values()
    for d in data:
        brewer = [kv for kv in d['tags'] if kv['key'] == 'brand']
        brewers = ' '.join(brewer['value'])
        d['longname'] = ' '.join([brewers, d['name']])

    if resp.status_code == 200:
        return data
    else:
        return {'errors': resp.status_code, message='delivery_request_failed'}

def name_match(beer1, namelist):
    """
    beer1 is a dictionary returned by the call to brewerydb.
    namelist is the list of available beer longnames
    """

    return


def filter_available_beers(available_beers, filter_to_names):
    namelist = [beer['longname'] for beer in available_beers]

    return {'beers': [
        v for v in available_beers.itervalues() if
        any([f.lower() in v['name'].lower()
             for f in filter_to_names])
    ]}
