import os
import requests
import datetime as dt
import urllib
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
        'https://delivery.com/api/data/search?search_type=alcohol{}'
        '&order_time=ASAP&order_type=delivery&client_id=brewhacks2016'
        '&section=beer'
    )

    validate_delivery_request(request)
    query = base.format('&address={}'.format(
        urllib.quote(request['address'])
    ))

    return query

def get_available_beers(request):
    query = make_delivery_request(request)
    resp = requests.get(query)
    return resp.json()['data']['products']

def filter_available_beers(available_beers, filter_to_names):
    return [v for v in available_beers.itervalues() if
            v['name'] in filter_to_names]
