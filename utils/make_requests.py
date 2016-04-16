import os
import requests
import datetime as dt

def create_query(uid, **kwargs):

    kwargs[key] = API_KEY
    base = 'http://api.brewerydb.com/v2/beer/'
    append = '&'.join(
        ['='.join([k, v]) for k, v kwargs.items()]
    )
    return base + append
