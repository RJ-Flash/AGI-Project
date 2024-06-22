import unittest
from src.rag.generator import Generator

class TestGenerator(unittest.TestCase):
    def test_generate(self):
        generator = Generator()
        self.assertEqual(generator.generate("AI is the future because"), "Generated text based on context: AI is the future because")

if __name__ == "__main__":
    unittest.main()
