import json
from flask import Flask, request
from flask.ext.cors import CORS
from utils.validation import (
    validate_beer_request
)

app = Flask(__name__)
CORS(app)

@route('/beer', methods=['POST'])
def get_beers():
    validate_beer_request(request)
    pass

