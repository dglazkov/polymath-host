import argparse
import os
import traceback

import numpy as np
import pinecone
import polymath
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_compress import Compress
from polymath.library import vector_from_base64

DEFAULT_TOKEN_COUNT = 1000

app = Flask(__name__)
Compress(app)

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = "us-west1-gcp"  # TODO: Make this configurable

config = polymath.host_config()

@app.route("/", methods=["POST"])
def start():
    try:
        library = polymath.Library()
        if library.embedding_model != request.form.get("query_embedding_model"):
            raise Exception("Library embedding model mismatch")
        if library.version != request.form.get('version', -1, type=int):
            raise Exception("Library version mismatch")
        query_embedding = request.form.get("query_embedding")
        count = request.form.get(
            "count", DEFAULT_TOKEN_COUNT, type=int)
        count_type = request.form.get("count_type")
        sort = request.form.get('sort')            
        sort_reversed = request.form.get('sort_reversed') is not None
        seed = request.form.get('seed')
        omit = request.form.get('omit')
        access_token = request.form.get('access_token', '')
        library.omit = 'embedding'
        pinecone.init(
            api_key=PINECONE_API_KEY,
            environment=PINECONE_ENVIRONMENT)
        index = pinecone.Index('polymath')
        embedding = vector_from_base64(query_embedding).tolist() if sort == 'similarity' else np.random.rand(1536).tolist()
        result = index.query(
            namespace=config['pinecone']['namespace'],
            top_k=10,
            include_metadata=True,
            vector=embedding
        )
        for item in result['matches']:
            bit = polymath.Bit(data={
                'id': item['id'],
                'text': item['metadata']['text'],
                'token_count': item['metadata'].get('token_count'),
                'access_tag': item['metadata'].get('access_tag'),
                'info': {
                    'url': item['metadata']['url'],
                    'image_url': item['metadata'].get('image_url'),
                    'title': item['metadata'].get('title'),
                    'description': item['metadata'].get('description'),
                }
            })
            library.insert_bit(bit)
        return jsonify(library.serializable())

    except Exception as e:
        return jsonify({
            "error": f"{e}\n{traceback.print_exc()}"
        })


@app.route("/", methods=["GET"])
def start_sample():
    return render_template("query.html", config=config)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--port', help='Number of the port to run the server on (8080 by default).', default=8080, type=int)
    args = parser.parse_args()
    app.run(host='127.0.0.1', port=args.port, debug=True)
