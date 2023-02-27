import argparse
import traceback
from urllib.parse import urlparse

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_compress import Compress
from flask_cors import CORS
from google.cloud import firestore
from polymath.pinecone import PineconeLibrary

DEFAULT_TOKEN_COUNT = 1000

app = Flask(__name__)
CORS(app)
Compress(app)

load_dotenv()
PINECONE_ENVIRONMENT = "us-west1-gcp"  # TODO: Make this configurable


class ConfigStore:
    def __init__(self):
        db = firestore.Client()
        self.sites = db.collection('sites')

    def get(self, base_url):
        slug = urlparse(base_url).hostname.split('.')[0]
        return self.sites.document(slug).get().to_dict()


store = ConfigStore()


def make_args(request):
    content_type = request.headers.get('Content-Type')
    args = {}
    if (content_type == 'application/json'):
        json = request.json
        if not json:
            return jsonify({
                "error": "No arguments provided"
            })
        args = {
            'count': DEFAULT_TOKEN_COUNT,
            **json
        }
    else:
        args = {
            'count': DEFAULT_TOKEN_COUNT,
            **request.form.to_dict()
        }
    return args


@app.route("/", methods=["POST"])
def start():
    try:
        config = store.get(request.base_url)
        library = PineconeLibrary(config["pinecone"])
        args = make_args(request)
        result = library.query(args)
        return jsonify(result.serializable())

    except Exception as e:
        return jsonify({
            "error": f"{e}\n{traceback.format_exc()}"
        })


@app.route("/", methods=["GET"])
def start_sample():
    config = store.get(request.base_url)
    return render_template("query.html", config=config)


@app.route('/_ah/warmup')
def warmup():
    return ('', 204)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--port', help='Number of the port to run the server on (8080 by default).', default=8080, type=int)
    args = parser.parse_args()
    app.run(host='127.0.0.1', port=args.port, debug=True)
