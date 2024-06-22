import unittest
from src.nlp.language_understanding import LanguageUnderstanding

class TestLanguageUnderstanding(unittest.TestCase):
    def test_understand(self):
        lu = LanguageUnderstanding()
        self.assertTrue("understood" in lu.understand("AI is [MASK]."))
        self.assertTrue("understood" in lu.understand("Hello [MASK]."))

if __name__ == "__main__":
    unittest.main()
