import pytest
import urllib
import requests
from ..utils.make_requests import (
    make_delivery_request, get_available_beers,
    filter_available_beers
)

def test_make_delivery_request():
    request = {'address': '1129 E 14th St, New York, New York'}
    req = make_delivery_request(request)
    assert req == (
        'https://delivery.com/api/data/search?search_type=alcohol'
        '&address=' + urllib.quote(request['address']) +
        '&order_time=ASAP&order_type=delivery&client_id=brewhacks2016'
        '&section=beer'
    )

    resp = requests.get(req)
    assert resp.status_code == 200

def test_get_beers():
    request = {'address': '1129 E 14th St, New York, New York'}
    acceptable_beers = ['Pabst Blue Ribbon Beer',
                        'Kingfisher Premium Lager']
    available_beers = get_available_beers(request)
    filtered = filter_available_beers(available_beers, acceptable_beers)
    assert set([x['name'] for x in filtered]) == set(acceptable_beers)
