
import re

def validate_email_address(email_address):
    email_re = re.compile(
        r'^\w+@\w+\.(com|edu|org|gov|net)$'
    )
    if not email_re.match(email_address):
        raise ValueError('bad email address passed')
