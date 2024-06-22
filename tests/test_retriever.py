import unittest
from src.rag.retriever import Retriever

class TestRetriever(unittest.TestCase):
    def test_retrieve(self):
        retriever = Retriever()
        retriever.add_documents(["AI is the future", "Machine learning is a subset of AI"])
        self.assertIn("AI is the future", retriever.retrieve("AI"))
        self.assertIn("Machine learning is a subset of AI", retriever.retrieve("AI"))
        self.assertIn("AI is the future", retriever.retrieve("future"))
        self.assertNotIn("unknown", retriever.retrieve("unknown"))

if __name__ == "__main__":
    unittest.main()
