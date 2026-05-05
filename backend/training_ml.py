import os
import json
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report
from data_preprocessing import DataPreprocessor
from feature_engineering import FeatureEngineer
from models.random_forest_model import RFModel
from models.xgboost_model import XGBModel
from models.svm_model import SVMModel
from models.ensemble import EnsembleModel

def calculate_metrics(y_true, y_pred, y_prob):
    return {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, average='weighted'),
        'recall': recall_score(y_true, y_pred, average='weighted'),
        'f1': f1_score(y_true, y_pred, average='weighted'),
        'roc_auc': roc_auc_score(y_true, y_prob[:, 1]) if y_prob.shape[1] > 1 else 0.0
    }

def train_all_models(data_path: str, target_col: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Preprocessing
    preprocessor = DataPreprocessor()
    df = preprocessor.load_data(data_path)
    
    # Feature Engineering
    fe = FeatureEngineer()
    df_engineered = fe.add_engineered_features(df)
    
    X_train, X_test, y_train, y_test = preprocessor.fit_transform(df_engineered, target_col)
    
    # Feature Selection
    X_train_selected = fe.select_features(X_train, y_train)
    X_test_selected = fe.transform_features(X_test)
    
    # Save preprocessor and feature engineer state
    preprocessor.save(os.path.join(output_dir, 'preprocessor.pkl'))
    import joblib
    joblib.dump(fe, os.path.join(output_dir, 'feature_engineer.pkl'))

    metrics = {}

    # 2. Train Models
    # RF
    rf = RFModel()
    rf.train(X_train_selected, y_train)
    rf.save(os.path.join(output_dir, 'rf_model.pkl'))
    
    y_pred_rf = rf.predict(X_test_selected)
    y_prob_rf = rf.predict_proba(X_test_selected)
    metrics['RandomForest'] = calculate_metrics(y_test, y_pred_rf, y_prob_rf)

    # XGBoost
    xgb_model = XGBModel()
    xgb_model.train(X_train_selected, y_train, X_test_selected, y_test)
    xgb_model.save(os.path.join(output_dir, 'xgb_model.json'))
    
    y_pred_xgb = xgb_model.predict(X_test_selected)
    y_prob_xgb = xgb_model.predict_proba(X_test_selected)
    metrics['XGBoost'] = calculate_metrics(y_test, y_pred_xgb, y_prob_xgb)

    # SVM
    svm_model = SVMModel()
    svm_model.train(X_train_selected, y_train)
    svm_model.save(os.path.join(output_dir, 'svm_model.pkl'))
    
    y_pred_svm = svm_model.predict(X_test_selected)
    y_prob_svm = svm_model.predict_proba(X_test_selected)
    metrics['SVM'] = calculate_metrics(y_test, y_pred_svm, y_prob_svm)

    # Ensemble
    ensemble = EnsembleModel(
        models=[('rf', rf), ('xgb', xgb_model), ('svm', svm_model)],
        weights=[1, 1.5, 0.5]
    )
    ensemble.train(X_train_selected, y_train)
    ensemble.save(os.path.join(output_dir, 'ensemble_model.pkl'))

    y_pred_ens = ensemble.predict(X_test_selected)
    y_prob_ens = ensemble.predict_proba(X_test_selected)
    metrics['Ensemble'] = calculate_metrics(y_test, y_pred_ens, y_prob_ens)

    # Save metrics
    with open(os.path.join(output_dir, 'model_metrics.json'), 'w') as f:
        json.dump(metrics, f, indent=4)
        
    print("Training complete. Models and metrics saved.")

if __name__ == "__main__":
    # Example usage:
    # train_all_models("data/patient_data.csv", "disease_target", "saved_models")
    pass
