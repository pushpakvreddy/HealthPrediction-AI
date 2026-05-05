import os
import joblib
import pandas as pd
import numpy as np
from data_preprocessing import DataPreprocessor
from feature_engineering import FeatureEngineer
from models.ensemble import EnsembleModel

class MLInference:
    def __init__(self, models_dir: str):
        self.models_dir = models_dir
        self.preprocessor = None
        self.fe = None
        self.model = None
        
        try:
            if os.path.exists(os.path.join(models_dir, 'preprocessor.pkl')):
                self.preprocessor = DataPreprocessor.load(os.path.join(models_dir, 'preprocessor.pkl'))
            if os.path.exists(os.path.join(models_dir, 'feature_engineer.pkl')):
                self.fe = joblib.load(os.path.join(models_dir, 'feature_engineer.pkl'))
            if os.path.exists(os.path.join(models_dir, 'ensemble_model.pkl')):
                self.model = EnsembleModel([], []) # Empty init
                self.model.load(os.path.join(models_dir, 'ensemble_model.pkl'))
        except Exception as e:
            print(f"Warning: Could not load ML models: {e}")

    def predict(self, df_input: pd.DataFrame) -> dict:
        """
        Runs inference on new data.
        Returns prediction, probability, and dummy feature contributions.
        """
        if not self.model or not self.preprocessor or not self.fe:
            return {
                "prediction": 0,
                "probability": 0.95, # Mock for testing
                "contributions": {"demo": 1.0},
                "warning": "Model not loaded. Using mock results."
            }
        try:
            # Preprocess
            df_eng = self.fe.add_engineered_features(df_input)
            X_processed = self.preprocessor.transform(df_eng)
            X_selected = self.fe.transform_features(X_processed)

            # Predict
            prediction = self.model.predict(X_selected)
            probability = self.model.predict_proba(X_selected)

            # Feature contributions (approximation for ensemble or just using top K selected names)
            # In a real scenario, SHAP values would be ideal.
            contributions = {f"feature_{i}": float(val) for i, val in enumerate(X_selected[0][:5])}

            return {
                "prediction": int(prediction[0]),
                "probability": float(np.max(probability[0])),
                "contributions": contributions
            }
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    pass
