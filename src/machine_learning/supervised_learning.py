from sklearn.linear_model import LogisticRegression

# This module handles supervised learning

class SupervisedLearning:
    def __init__(self):
        self.model = LogisticRegression()

    def train(self, data, labels):
        try:
            self.model.fit(data, labels)
        except Exception as e:
            print(f"Training error: {e}")

    def predict(self, new_data):
        try:
            return self.model.predict(new_data).tolist()
        except Exception as e:
            print(f"Prediction error: {e}")
            return []
