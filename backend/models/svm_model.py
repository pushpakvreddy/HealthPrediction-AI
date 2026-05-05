from sklearn.svm import SVC
import joblib

class SVMModel:
    def __init__(self):
        self.model = SVC(
            kernel='rbf',
            probability=True,
            random_state=42
        )

    def train(self, X_train, y_train):
        """Trains the SVM model."""
        self.model.fit(X_train, y_train)

    def predict(self, X):
        """Predicts classes."""
        return self.model.predict(X)

    def predict_proba(self, X):
        """Predicts class probabilities."""
        return self.model.predict_proba(X)

    def save(self, filepath: str):
        joblib.dump(self.model, filepath)

    def load(self, filepath: str):
        self.model = joblib.load(filepath)
