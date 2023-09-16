from flask import Flask, request
import requests

import os

app = Flask(__name__)


@app.route('/ingest_document', methods=['POST'])
def ingest_document():
    content = request.json['content']

    # Get the embedding from embedder_service
    response = requests.post(f"http://embedder:{os.environ['EMBEDDING_SERVICE_PORT']}/embed",
                             json={'text': content})
    embedding = response.json().get('embedding')

    # Add the document to the db_service and get its ID
    response = requests.post(f"http://doc_db:{os.environ['DB_SERVICE_PORT']}/add_document",
                             json={'content': content})
    doc_id = response.json().get('doc_id')

    # Add the embedding to the search_service (which will also update the mapping in db_service)
    response = requests.post(f"http://searcher:{os.environ['SEARCH_SERVICE_PORT']}/add_embedding",
                             json={'embedding': embedding, 'doc_id': doc_id})

    return response.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ['INGESTION_SERVICE_PORT'])