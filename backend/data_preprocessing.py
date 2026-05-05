import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from typing import Tuple, Dict, Any
import joblib

class DataPreprocessor:
    def __init__(self, n_neighbors: int = 5):
        self.imputer = KNNImputer(n_neighbors=n_neighbors)
        self.scaler = StandardScaler()
        self.encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        
        # Save categorical columns and numerical columns states
        self.categorical_cols = None
        self.numerical_cols = None
        self.feature_names = None

    def load_data(self, filepath: str) -> pd.DataFrame:
        """Loads data from a CSV file."""
        try:
            return pd.read_csv(filepath)
        except Exception as e:
            raise Exception(f"Error loading data from {filepath}: {str(e)}")

    def fit_transform(self, df: pd.DataFrame, target_col: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Fits the preprocessor on the data and returns train/test splits."""
        if target_col not in df.columns:
            raise ValueError(f"Target column '{target_col}' not found in dataframe.")

        # Separate features and target
        X = df.drop(columns=[target_col])
        y = df[target_col].values

        self.categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
        self.numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

        # Handle missing values using KNNImputer for numericals
        if self.numerical_cols:
            X[self.numerical_cols] = self.imputer.fit_transform(X[self.numerical_cols])

        # Normalize features
        if self.numerical_cols:
            X[self.numerical_cols] = self.scaler.fit_transform(X[self.numerical_cols])

        # One-hot encode categorical variables
        if self.categorical_cols:
            encoded_cats = self.encoder.fit_transform(X[self.categorical_cols])
            cat_feature_names = self.encoder.get_feature_names_out(self.categorical_cols)
            
            # Combine back
            X_num = X[self.numerical_cols].values if self.numerical_cols else np.empty((X.shape[0], 0))
            X_processed = np.hstack((X_num, encoded_cats))
            self.feature_names = self.numerical_cols + list(cat_feature_names)
        else:
            X_processed = X[self.numerical_cols].values
            self.feature_names = self.numerical_cols

        # Train-test split (80-20)
        X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)

        return X_train, X_test, y_train, y_test

    def transform(self, df: pd.DataFrame) -> np.ndarray:
        """Transforms new data using the fitted preprocessor."""
        if self.feature_names is None:
            raise Exception("Preprocessor has not been fitted yet.")

        X = df.copy()

        # Handle missing values
        if self.numerical_cols:
            # For transform, we might need a simpler imputation if KNN is too slow for single records, 
            # but we'll stick to the fitted KNN imputer here.
            X[self.numerical_cols] = self.imputer.transform(X[self.numerical_cols])
            X[self.numerical_cols] = self.scaler.transform(X[self.numerical_cols])

        if self.categorical_cols:
            encoded_cats = self.encoder.transform(X[self.categorical_cols])
            X_num = X[self.numerical_cols].values if self.numerical_cols else np.empty((X.shape[0], 0))
            X_processed = np.hstack((X_num, encoded_cats))
        else:
            X_processed = X[self.numerical_cols].values

        return X_processed

    def save(self, filepath: str):
        """Saves the preprocessor to disk."""
        joblib.dump(self, filepath)

    @classmethod
    def load(cls, filepath: str):
        """Loads a preprocessor from disk."""
        return joblib.load(filepath)
