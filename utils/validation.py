import re

def validate_email_address(email_address):
    email_re = re.compile(
        r'^\w+@\w+\.(com|edu|org|gov|net)$'
    )
    if not email_re.match(email_address):
        raise ValueError('bad email address passed')

def validate_delivery_request(request):
    assert 'address' in request
    assert request['address']

def validate_beer_request(request):
    assert 'name' in request or 'abv' in request or 'ibv' in request or 'srmId' in request or 'availabilityId' in request or 'styleId' in request
