import unittest
from src.knowledge_representation.symbolic_reasoning import SymbolicReasoning

class TestSymbolicReasoning(unittest.TestCase):
    def test_reason(self):
        reasoning = SymbolicReasoning()
        reasoning.add_premise("AI is powerful")
        self.assertEqual(reasoning.reason(["AI"]), ["AI is powerful"])
        self.assertEqual(reasoning.reason(["not in premise"]), [])

if __name__ == "__main__":
    unittest.main()
