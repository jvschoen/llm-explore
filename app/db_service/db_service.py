from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DOCUMENTS_DB = 'documents.db'
MAPPING_DB = 'mapping.db'
def init_db():
    conn = sqlite3.connect(DOCUMENTS_DB)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            doc_id INTEGER PRIMARY KEY,
            content TEXT
        )
        """)
    conn.commit()
    conn.close()

    conn = sqlite3.connect(MAPPING_DB)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            faiss_index_position INTEGER PRIMARY KEY,
            doc_id TEXT
        )
        """)
    conn.commit()
    conn.close()

init_db()

@app.route('/get_documents', methods=['POST'])
def get_documents():
    """
    This gets all documents that match a list of doc ids

    Table returned
    doc_id | content

    JSON response:
    {documents: [{doc_id: content}, ...]}
    """

    doc_ids = request.json['doc_ids']
    placeholder = ', '.join('?' for _ in doc_ids)

    conn = sqlite3.connect(DOCUMENTS_DB)
    cursor = conn.cursor()
    cursor.execute(
        f"""
        SELECT * FROM documents
        WHERE doc_id IN ({placeholder})""",
        doc_ids
    )
    docs = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()

    return jsonify({'documents': docs})

@app.rout('/get_document_ids', methods=['POST'])
def get_document_ids(doc_ids):
    """
    This gets all document ids where the faiss index matches.
    There may be many Faiss indexes (embedding vectors) that
    map to any single document. We chunk our input docs into
    token sizes (<512) to meet embedding model's constraints.

    Table Returned
    doc_id

    JSON response:
    {documents: [{doc_id: content}, ...]}
    """

    placeholder = ', '.join('?' for _ in doc_ids)
    conn = sqlite3.connect(MAPPING_DB)
    cursor = conn.cursor()

    cursor.execute(
        f"""
        SELECT doc_id FROM mapping
        WHERE faiss_index_position IN ({placeholder})
        """)
    fetched_docs = cursor.fetchall()
    doc_ids = [row[0] for row in fetched_docs]
    conn.close()

    return jsonify({'doc_ids': doc_ids})

@app.route('/add_document', method=['POST'])
def add_document():
    """
    expected {'content': 'full document of text'}
    """
    content = request.json['content']

    conn = sqlite3.connect(DOCUMENTS_DB)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO documents (content) VALUES (?)", (content, ))
    doc_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return jsonify({'doc_id': doc_id})


@app.route('/add_mapping', methods=['POST'])
def add_mapping():

    faiss_index_position = request.json['faiss_index_position']
    doc_id = request.json['doc_id']

    conn = sqlite3.connect('mapping.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO mapping (faiss_index_position, doc_id) VALUES (?, ?)",
                   (faiss_index_position, doc_id))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)