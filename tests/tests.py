import pytest
import urllib
import requests
from ..utils.make_requests import (
    make_delivery_request, filter_available_beers
)

class MockRequest(object):
    args = {'address': '1129 E 14th St, New York, New York'}

def test_make_delivery_request():
    request = MockRequest()
    resp = make_delivery_request(request)
    assert isinstance(resp, dict)
    assert len(resp.keys()) > 0

def test_get_beers():
    request = MockRequest()
    acceptable_beers = ['Pabst Blue Ribbon Beer',
                        'Kingfisher Premium Lager']
    available_beers = make_delivery_request(request)
    filtered = filter_available_beers(available_beers, acceptable_beers)
    assert set([x['name'] for x in filtered['beers']]) == set(acceptable_beers)
