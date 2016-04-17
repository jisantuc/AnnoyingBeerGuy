import os
import requests
import datetime as dt
import urllib
import json
from fuzzywuzzy import process
from validation import validate_beer_request, validate_delivery_request

def create_brewerydb_query(request):
    req = dict(request.values.items())
    validate_beer_request(req)
    base = 'http://api.brewerydb.com/v2/beers'
    req.update({'key': os.environ['API_KEY'],
                'withBreweries': 'Y'})

    response = requests.get(base, params=req).json()
    data = response['data']
    if response['numberOfPages'] > 1:
        for p in range(2, min(10, int(response['numberOfPages'])) + 1):
            req.update({'p': p})
            data.extend(requests.get(base, req).json()['data'])

    def _get_brewer(beer):
        if 'breweries' in beer:
            return ' '.join([b['name'] for b in beer['breweries']])
        else:
            return ''

    beer_names = [
        {'name': d['name'],
         'abv': d['abv'],
         'brewer': _get_brewer(d),
         'organic': d['isOrganic']}
        for d in data
    ]

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
        brewer = [kv for kv in d['tags'] if kv['key'] == 'brand'][0]
        brewers = ' '.join(brewer['value'])
        d['longname'] = ' '.join([brewers, d['name']])

    if resp.status_code == 200:
        return data
    else:
        return {'errors': resp.status_code, message: 'delivery_request_failed'}

def filter_available_beers(available_beers, all_beers):

    orig_len = len(all_beers)
    namelist = [beer['longname'] for beer in all_beers]
    for beer_av in available_beers:
        name, score = process.extractOne(beer['longname'], namelist)
        print name, score
        if score > 80:
            match = [beer for beer in all_beers if beer['longname'] == name][0]
            index = all_beers.index(match)
            match['available'] = True
            match['productId'] = beer_av['product_id']
            match['merchantId'] = beer_av['merchant_id']
            match['link'] = ('https://delivery.com/api/data/product/'
                             '{}?merchant_id={}&show_description=true'
                             '&client_id=brewhacks2016').format(
                                 match['productId'], match['merchantId']
                             )
            all_beers[index] = match

    for beer in all_beers:
        if 'available' not in beer:
            beer['available'] = False

    assert len(all_beers) == orig_len

    return {'beers': all_beers}
