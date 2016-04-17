import json
import os
from flask import Flask, request, jsonify
from flask.ext.cors import CORS
from utils.make_requests import (
    make_delivery_request, filter_available_beers, create_brewerydb_query
)

port = int(os.getenv('VCAP_APP_PORT', 8080))
if not os.getenv('API_KEY'):
    os.environ['API_KEY'] = 'YOUR_API_KEY'

app = Flask(__name__)
CORS(app)

@app.route('/beer', methods=['GET', 'POST'])
def get_beers():
    available_beers = make_delivery_request(request)
    acceptable_beers = create_brewerydb_query(request)

    return jsonify(
        filter_available_beers(available_beers, acceptable_beers)
    )

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return 'hello!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
