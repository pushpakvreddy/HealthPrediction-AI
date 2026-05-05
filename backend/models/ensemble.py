import numpy as np
from sklearn.ensemble import VotingClassifier
import joblib

class EnsembleModel:
    def __init__(self, models: list, weights: list = None):
        """
        models: List of tuples ('name', model_instance)
        weights: List of weights for each model
        """
        # We need the underlying sklearn/xgboost models
        estimators = []
        for name, m in models:
            # Assume m has a .model attribute which is the underlying scikit-learn compatible estimator
            estimators.append((name, m.model))
            
        self.model = VotingClassifier(
            estimators=estimators,
            voting='soft',
            weights=weights
        )

    def train(self, X_train, y_train):
        """Trains the ensemble model."""
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
