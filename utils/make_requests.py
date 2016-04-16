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
    )

    validate_delivery_request(request)

    if 'address' in request:
        query = base.format('&address={}'.format(
            urllib.quote(request['address'])
        ))
    else:
        query = base.format('&longitude={}&latitude={}'.format(
            request['longitude'], request['latitude']
        ))

    return query

def get_available_beers(request):
    query = make_delivery_request(request)
    return requests.get(query)
