# TODO: rename this to faiss service since we add and search
from flask import Flask, request, jsonify
import requests
import atexit
import os

import numpy as np
import faiss


GET_DOC_IDS_URL = f'http://doc_db:{os.environ["DB_SERVICE_PORT"]}/get_document_ids'
GET_DOCS_URL = f'http://doc_db:{os.environ["DB_SERVICE_PORT"]}/get_documents'
ADD_MAPPING_URL = f'http://doc_db:{os.environ["DB_SERVICE_PORT"]}/add_mapping'

app = Flask(__name__)
INDEX_PATH = "/app/index_data/faiss_index.index"

def init_faiss_index():
    if not os.path.exists(INDEX_PATH):
        index = faiss.IndexFlatL2(384)
        faiss.write_index(index, INDEX_PATH)


def load_faiss_index():
    return faiss.read_index(INDEX_PATH)


@app.route('/search', methods=['POST'])
def search():
    """
    Returns the source documents that most closely relate
    to the user's input prompt
    """
    embedding = np.array(request.json['embedding']).reshape(1, -1)
    index = load_faiss_index()
    _, I = index.search(embedding, 5) # Top 5 closest embeddings
    indices = [int(index) for index in I[0]]

    # Pass over top 5 vector indices.
    # These indices map to source document ids
    response = requests.post(GET_DOC_IDS_URL,
                             json={'doc_ids': indices})
    matched_doc_ids = response.json().get('doc_ids')
    unique_doc_ids = list(set(matched_doc_ids))

    # The doc ids map to actual full document content text
    response = requests.post(GET_DOCS_URL,
                             json={'doc_ids': unique_doc_ids})
    docs = response.json().get('documents')

    return jsonify({'documents': docs})

@app.route('/add_embedding', methods=['POST'])
def add_embedding():
    embedding = np.array(request.json['embedding']).reshape(1, -1)
    doc_id = request.json['doc_id']

    index = load_faiss_index()
    faiss_index_position = index.ntotal
    index.add(embedding)

    # Update mapping database with the new relation
    response = requests.post(ADD_MAPPING_URL,
                             json={'faiss_index_position': faiss_index_position,
                                   'doc_id': doc_id})

    return response.json()

# Ensure the FAISS index gets persisted after adding new data
def save_faiss_index():
    index = load_faiss_index()
    faiss.write_index(index, INDEX_PATH)

init_faiss_index()

if __name__ == '__main__':
    atexit.register(save_faiss_index)
    app.run(host='0.0.0.0', port=os.environ['SEARCH_SERVICE_PORT'])