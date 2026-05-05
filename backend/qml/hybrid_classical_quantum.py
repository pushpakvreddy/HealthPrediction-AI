import numpy as np
from sklearn.preprocessing import MinMaxScaler
from .vqe_optimizer import VQEOptimizer
from .quantum_circuits import feature_encoding_circuit

class HybridModel:
    def __init__(self):
        self.scaler = MinMaxScaler(feature_range=(0, np.pi))
        self.vqe = VQEOptimizer(layers=3)
        self.optimal_weights = None

    def preprocess_features(self, features):
        """
        Scales features to [0, pi] for angle encoding.
        features: numpy array of shape (n_samples, n_features)
        """
        # Ensure we have exactly 4 features for the 4-qubit circuit
        if features.shape[1] > 4:
            # Simple PCA or selection could go here, for now just slice
            features = features[:, :4]
        elif features.shape[1] < 4:
            # Pad with zeros
            pad = np.zeros((features.shape[0], 4 - features.shape[1]))
            features = np.hstack([features, pad])
            
        return self.scaler.fit_transform(features)

    def train(self, features, target_efficacy):
        """
        Trains the quantum circuit using VQE.
        Since VQE optimizes for a single instance typically or we aggregate,
        we'll simplify by optimizing for the average of the dataset or a specific patient.
        """
        processed_features = self.preprocess_features(features)
        
        # Simple approach: train on first sample
        # In a real scenario, you'd define a batched cost function
        sample_features = processed_features[0]
        sample_target = target_efficacy[0]
        
        self.optimal_weights, cost_history = self.vqe.optimize(sample_features, sample_target, iterations=100)
        return cost_history

    def predict(self, features):
        """
        Predicts efficacy using the optimized quantum circuit.
        """
        if self.optimal_weights is None:
            raise Exception("Model must be trained first.")
            
        processed_features = self.scaler.transform(features[:, :4])
        
        predictions = []
        for i in range(processed_features.shape[0]):
            exp_vals = feature_encoding_circuit(processed_features[i], self.optimal_weights)
            # Map expectation [-1, 1] to [0, 1] efficacy score
            efficacy = (float(exp_vals[0]) + 1) / 2
            predictions.append(efficacy)
            
        return np.array(predictions)
