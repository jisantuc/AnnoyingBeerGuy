import requests
import datetime as dt

API_KEY = 'YOUR_API_KEY'

def create_query(uid, **kwargs):

    kwargs[key] = API_KEY
    base = 'http://api.brewerydb.com/v2/beer/'
    append = '&'.join(
        ['='.join([k, v]) for k, v kwargs.items()]
    )
    return base + append
