from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

EMBEDDING_SERVICE_URL = "http://embedder:5001/embed" # Embedding service on port 5001
SEARCH_SERVICE_URL = 'http://searcher:5002/search'
INGEST_DOC_SERVICE_URL = "http://ingestion_service:5004/ingest_document"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            result = ingest_doc(file)
            return result

        elif 'prompt' in request.form:
            prompt = request.form['prompt']
            embedding = get_embedding(prompt)
            docs = search_documents(embedding)
        # Logic to handle embedding and communicate wiht other services here
            return render_template('results.html', document_ids=docs)
    return render_template('index.html')

def ingest_doc(file):
    content = file.read().decode('utf-8')
    response = requests.post(INGEST_DOC_SERVICE_URL, json={'content': content})
    return jsonify(response.json())


def get_embedding(text):
    response = requests.post(EMBEDDING_SERVICE_URL, json={'text': text})
    return response.json().get('embedding')


def search_documents(embedding):
    response = requests.post(SEARCH_SERVICE_URL, json={'embedding': embedding})
    return response.json().get('documents')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)