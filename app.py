import json
from flask import Flask, request, jsonify
from flask.ext.cors import CORS
from utils.make_requests import (
    make_delivery_request, filter_available_beers, create_brewerydb_query
)
from tests.tests import test_create_brewery_db_query

app = Flask(__name__)
CORS(app)

@app.route('/beer', methods=['GET', 'POST'])
def get_beers():
    acceptable_beers = create_brewerydb_query(request)

    available_beers = make_delivery_request(request)

    return jsonify(
        filter_available_beers(available_beers, acceptable_beers)
    )

test_create_brewery_db_query()

if __name__ == '__main__':
    app.run(debug=True)
