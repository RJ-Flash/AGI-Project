import unittest
from src.machine_learning.supervised_learning import SupervisedLearning

class TestSupervisedLearning(unittest.TestCase):
    def test_predict(self):
        model = SupervisedLearning()
        data = [[0], [1], [2]]
        labels = [0, 1, 1]
        model.train(data, labels)
        self.assertEqual(model.predict([[1], [2]]), [1, 1])

if __name__ == "__main__":
    unittest.main()
