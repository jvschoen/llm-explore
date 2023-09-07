from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import os

app = Flask(__name__)

@app.route('/embed', methods=['POST'])
def embed():
    # Use Sentence Transformer here
    text = request.json['text']
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    # reduces amount of api calls to huggingface
    if not os.path.exists('sentence-transformers/all-MiniLM-L6-v2'):
        model.save('sentence-transformers/all-MiniLM-L6-v2')

    embedding = model.encode(text)

    return jsonify({"embedding": embedding})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)