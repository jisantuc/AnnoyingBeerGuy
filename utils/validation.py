import re

def validate_email_address(email_address):
    email_re = re.compile(
        r'^\w+@\w+\.(com|edu|org|gov|net)$'
    )
    if not email_re.match(email_address):
        raise ValueError('bad email address passed')

def validate_delivery_request(requestdata):
    assert 'address' in requestdata
    assert requestdata['address']

def validate_beer_request(requestdata):
    assert ('name' in requestdata or 'abv' in requestdata or
            'ibu' in requestdata or 'srmId' in requestdata or
            'availabilityId' in requestdata or 'styleId' in requestdata)
