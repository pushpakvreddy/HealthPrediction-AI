import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif

class FeatureEngineer:
    def __init__(self, k_best: int = 10):
        self.k_best = k_best
        self.selector = SelectKBest(score_func=f_classif, k=k_best)
        self.selected_indices = None

    def add_engineered_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Adds BMI categories, age groups, and interaction features."""
        df_new = df.copy()

        # BMI Categories (assuming bmi column exists)
        if 'bmi' in df_new.columns:
            conditions = [
                (df_new['bmi'] < 18.5),
                (df_new['bmi'] >= 18.5) & (df_new['bmi'] < 25),
                (df_new['bmi'] >= 25) & (df_new['bmi'] < 30),
                (df_new['bmi'] >= 30)
            ]
            choices = ['Underweight', 'Normal', 'Overweight', 'Obese']
            df_new['bmi_category'] = np.select(conditions, choices, default='Unknown')

        # Age Groups (assuming age column exists)
        if 'age' in df_new.columns:
            bins = [0, 18, 35, 50, 65, 120]
            labels = ['Child', 'Young Adult', 'Adult', 'Middle Age', 'Senior']
            df_new['age_group'] = pd.cut(df_new['age'], bins=bins, labels=labels, right=False)

        # Interaction Feature (example: age * cholesterol)
        if 'age' in df_new.columns and 'cholesterol' in df_new.columns:
            df_new['age_cholesterol_interaction'] = df_new['age'] * df_new['cholesterol']

        # Statistical features (mean/std of vital signs)
        vitals = [col for col in ['heart_rate', 'bp_sys', 'bp_dia', 'spo2', 'temp'] if col in df_new.columns]
        if len(vitals) > 1:
            df_new['vitals_mean'] = df_new[vitals].mean(axis=1)
            df_new['vitals_std'] = df_new[vitals].std(axis=1)

        return df_new

    def select_features(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Selects top K features using ANOVA F-value."""
        X_selected = self.selector.fit_transform(X, y)
        self.selected_indices = self.selector.get_support(indices=True)
        return X_selected

    def transform_features(self, X: np.ndarray) -> np.ndarray:
        """Transforms new data using the fitted feature selector."""
        if self.selected_indices is None:
            raise Exception("Feature selector has not been fitted yet.")
        return X[:, self.selected_indices]
