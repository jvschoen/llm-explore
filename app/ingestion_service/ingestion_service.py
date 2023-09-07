from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/ingest_document', methods=['POST'])
def ingest_document():
    content = request.json['content']

    # Get the embedding from embedder_service
    response = requests.post("http://embedder_service:5001/embed", json={'text': content})
    embedding = response.json().get('embedding')

    # Add the document to the db_service and get its ID
    response = requests.post("http://db_service:5003/add_document", json={'content': content})
    doc_id = response.json().get('doc_id')

    # Add the embedding to the search_service (which will also update the mapping in db_service)
    response = requests.post("http://search_service:5002/add_embedding", json={'embedding': embedding, 'doc_id': doc_id})

    return response.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)