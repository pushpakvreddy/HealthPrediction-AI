import xgboost as xgb
import joblib

class XGBModel:
    def __init__(self):
        self.model = xgb.XGBClassifier(
            learning_rate=0.1,
            max_depth=6,
            n_estimators=200,
            early_stopping_rounds=10,
            random_state=42,
            eval_metric='logloss'
        )

    def train(self, X_train, y_train, X_val, y_val):
        """Trains the XGBoost model with early stopping."""
        self.model.fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)],
            verbose=False
        )

    def predict(self, X):
        """Predicts classes."""
        return self.model.predict(X)

    def predict_proba(self, X):
        """Predicts class probabilities."""
        return self.model.predict_proba(X)

    def save(self, filepath: str):
        self.model.save_model(filepath)

    def load(self, filepath: str):
        self.model = xgb.XGBClassifier()
        self.model.load_model(filepath)
