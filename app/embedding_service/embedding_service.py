from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import os

app = Flask(__name__)
MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'

@app.route('/embed', methods=['POST'])
def embed():
    # Use Sentence Transformer here
    text = request.json['text']
    model = SentenceTransformer(MODEL_NAME)
    # reduces amount of api calls to huggingface
    if not os.path.exists(MODEL_NAME):
        model.save(MODEL_NAME)

    embedding = model.encode(text)
    print(embedding)

    return jsonify({"embedding": embedding.tolist()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ['EMBEDDING_SERVICE_PORT'])