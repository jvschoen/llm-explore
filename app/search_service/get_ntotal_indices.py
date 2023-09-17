import faiss
index = faiss.read_index("/app/index_data/faiss_index.index")
print(index.ntotal)