# This module handles the ontology and taxonomy for knowledge representation

class Ontology:
    def __init__(self):
        self.concepts = {}

    def add_concept(self, concept_name, description):
        self.concepts[concept_name] = description

    def get_concept(self, concept_name):
        return self.concepts.get(concept_name, "Concept not found")
