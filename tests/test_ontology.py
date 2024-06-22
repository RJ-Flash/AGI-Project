import unittest
from src.knowledge_representation.ontology import Ontology

class TestOntology(unittest.TestCase):
    def test_add_and_get_concept(self):
        ontology = Ontology()
        ontology.add_concept("AI", "Artificial Intelligence")
        self.assertEqual(ontology.get_concept("AI"), "Artificial Intelligence")
        self.assertEqual(ontology.get_concept("Unknown"), "Concept not found")

if __name__ == "__main__":
    unittest.main()
