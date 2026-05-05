from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import joblib

class RFModel:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            random_state=42
        )

    def train(self, X_train, y_train):
        """Trains the Random Forest model."""
        self.model.fit(X_train, y_train)

    def predict(self, X):
        """Predicts classes."""
        return self.model.predict(X)

    def predict_proba(self, X):
        """Predicts class probabilities."""
        return self.model.predict_proba(X)

    def get_feature_importance(self):
        """Returns feature importances."""
        return self.model.feature_importances_

    def save(self, filepath: str):
        joblib.dump(self.model, filepath)

    def load(self, filepath: str):
        self.model = joblib.load(filepath)
