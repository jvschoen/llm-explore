# Placeholder for Faiss index
index = faiss.IndexFlatL2(5) # Adjust dims based on embeddings

# Mock Up, the embeddings and ids should map to actual values
doc_embeddings = np.array([[65, 66, 67, 68, 69],
                           [70, 71, 72, 73, 74]])
doc_ids = [1, 2]

index.add(doc_embeddings)