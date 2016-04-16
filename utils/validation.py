
import re

def validate_email_address(email_address):
    email_re = re.compile(
        r'^\w+@\w+\.(com|edu|org|gov|net)$'
    )
    if not email_re.match(email_address):
        raise ValueError('bad email address passed')

def validate_delivery_request(request):
    if 'address' in request:
        assert request['address']
    else:
        assert 'latitude' in request
        assert 'longitude' in request
        assert request['latitude']
        assert request['longitude']


def validate_beer_request(request):
    pass
