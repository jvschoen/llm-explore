from flask import Flask, render_template, request, jsonify
import requests
import os
from io import BytesIO

from docx import Document
from pypdf import PdfReader

app = Flask(__name__)

EMBEDDING_SERVICE_URL = f'http://embedder:{os.environ["EMBEDDING_SERVICE_PORT"]}/embed' # Embedding service on port 5001
SEARCH_SERVICE_URL = f'http://searcher:{os.environ["SEARCH_SERVICE_PORT"]}/search'
INGEST_DOC_SERVICE_URL = f'http://ingestor:{os.environ["INGESTION_SERVICE_PORT"]}/ingest_document'
CLEAR_DBS_URL = f'http://doc_db:{os.environ["DB_SERVICE_PORT"]}/clear_dbs'

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        prompt = request.form.get('prompt')
        if prompt:
            embedding = get_embedding(prompt)
            docs = search_documents(embedding)
            message = f"Document Ids: {docs}"

        file = request.files.get('input_file')
        if file:
            result = ingest_doc(file)
            message = f'Uploading {file.filename}: {result}'

        clear_dbs_button = request.form.get('clear_dbs_button')
        if clear_dbs_button:
            result = clear_dbs()
            message = f'{result}: Cleared Mapping and Document DBs'

    return render_template('index.html', result=message)


def extract_text_from_file(file):

    filename = file.filename
    print(type(file))

    # Get file extension
    file_extension = os.path.splitext(filename)[1].lower()
    print(f'file extension: {file_extension}')

    # For Word documents
    if file_extension == '.docx':
        doc = Document(BytesIO(file.read()))
        return [p.text for p in doc.paragraphs if p.text.strip() != ""]

    # For PDFs
    elif file_extension == '.pdf':
        reader = PdfReader(file)
        return [reader.getPage(i).extractText() for i in range(reader.numPages)]

    # For plain text files
    # add more plain text formats if necessary
    elif file_extension in ['.txt', '.md', '.csv', '.tsv']:
        return file.read()

    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

def ingest_doc(file):

    content = str(extract_text_from_file(file))
    response = requests.post(INGEST_DOC_SERVICE_URL, json={'content': content})
    return jsonify(response.json())


def get_embedding(text):
    response = requests.post(EMBEDDING_SERVICE_URL, json={'text': text})
    return response.json().get('embedding')


def search_documents(embedding):
    response = requests.post(SEARCH_SERVICE_URL, json={'embedding': embedding})
    return response.json().get('documents')

def clear_dbs():
    response = requests.post(CLEAR_DBS_URL)
    return response.json()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ['WEB_SERVICE_PORT'])