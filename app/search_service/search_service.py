# TODO: rename this to faiss service since we add and search
from flask import Flask, request, jsonify
import requests
import atexit

import numpy as np
import faiss

GET_DOC_IDS_URL = 'http://db_service:5003/get_document_ids'
GET_DOCS_URL = 'http://db_service:5003/get_documents'
ADD_MAPPING_URL = "http://db_service:5003/add_mapping"

app = Flask(__name__)

# Load the FAISS index (assuming it's persisted somewhere)
index = faiss.read_index("faiss_index.index")

@app.route('/search', methods=['POST'])
def search():
    """
    Returns the source documents that most closely relate
    to the user's input prompt
    """
    embedding = np.array(request.json['embedding']).reshape(1, -1)
    _, I = index.search(embedding, 5) # Top 5 closest embeddings

    # Pass over top 5 vector indices.
    # These indices map to source document ids
    response = requests.post(GET_DOC_IDS_URL,
                             json={'indices': list(I[0])})
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

    faiss_index_position = index.ntotal
    index.add(embedding)

    # Update mapping database with the new relation
    response = requests.post(ADD_MAPPING_URL,
                             json={'faiss_index_position': faiss_index_position,
                                   'doc_id': doc_id})

    return response.json()

# Ensure the FAISS index gets persisted after adding new data
def save_faiss_index():
    faiss.write_index(index, 'faiss_index.index')

if __name__ == '__main__':
    atexit.register(save_faiss_index)
    app.run(host='0.0.0.0', port=5002)