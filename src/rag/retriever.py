from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# This module handles the retrieval component of Retrieval-Augmented Generation (RAG)

class Retriever:
    def __init__(self):
        self.documents = []
        self.vectorizer = TfidfVectorizer()
        self.doc_vectors = None

    def add_documents(self, docs):
        self.documents.extend(docs)
        self.doc_vectors = self.vectorizer.fit_transform(self.documents)

    def retrieve(self, query):
        if not self.documents:
            return []
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.doc_vectors).flatten()
        ranked_docs = [self.documents[i] for i in similarities.argsort()[::-1]]
        return ranked_docs
