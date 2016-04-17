import json, os, sendgrid
from flask import Flask, request, jsonify
from flask.ext.cors import CORS
from utils.make_requests import (
    make_delivery_request, filter_available_beers, create_brewerydb_query
)
from utils.caching import cache, load_cache_file_to_json

port = int(os.getenv('VCAP_APP_PORT', 8080))

if not os.getenv('API_KEY'):
    os.environ['API_KEY'] = 'YOUR_API_KEY'
if not os.getenv('SENDGRID_API_KEY'):
    os.environ['SENGRID_API_KEY'] = 'YOUR_API_KEY'

app = Flask(__name__)
CORS(app)

CACHE_LIST = []

@app.route('/beer', methods=['GET', 'POST'])
def get_beers():

    req = dict(request.values.items())

    if (req['address'], req['abv']) in CACHE_LIST:
        cached = load_cache_file_to_json('cache.txt')
        key = ' '.join((req['address'], req['abv']))
        match = [js for js in cached if key
                 in js.keys()][0]
        return jsonify(match[key])

    available_beers = make_delivery_request(request)
    acceptable_beers = create_brewerydb_query(request)

    results = filter_available_beers(available_beers, acceptable_beers,
                                     req['address'])

    cache(results, req['address'], req['abv'], CACHE_LIST)

    return jsonify(results)


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return 'hello'

@app.route('/subscribe', methods=['GET'])
def subscribe():
    client = sendgrid.SendGridClient(os.environ['SENDGRID_API_KEY'])
    message = sendgrid.Mail()

    req = dict(request.values.items())

    message.add_to(req['email'])
    message.set_from("annoying@beerguy.com")
    message.set_subject("Your beer subscription")
    message.set_html("Thanks for subscribing to Annoying Beer Guy! We'll keep you posted on beers that are available in your area.")

    client.send(message)

    return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
