import pennylane as qml
from pennylane import numpy as np
from .quantum_circuits import feature_encoding_circuit, get_num_weights

class VQEOptimizer:
    def __init__(self, layers=3):
        self.layers = layers
        self.weights_shape = get_num_weights(layers)
        self.opt = qml.AdamOptimizer(stepsize=0.1)

    def cost_function(self, weights, features, target_efficacy):
        """
        Cost function to minimize.
        For VQE context here, we want the circuit expectation value to match the target_efficacy.
        Expectation value of the first qubit is mapped to efficacy.
        """
        exp_vals = feature_encoding_circuit(features, weights)
        # Using expectation of first qubit as efficacy score [-1, 1] mapped to [0, 1]
        predicted_efficacy = (exp_vals[0] + 1) / 2
        return (predicted_efficacy - target_efficacy) ** 2

    def optimize(self, features, target_efficacy, iterations=100):
        """
        Runs the VQE optimization loop.
        """
        # Initialize random weights
        weights = np.random.uniform(low=-np.pi, high=np.pi, size=self.weights_shape, requires_grad=True)
        
        cost_history = []
        for i in range(iterations):
            weights, cost = self.opt.step_and_cost(lambda w: self.cost_function(w, features, target_efficacy), weights)
            cost_history.append(cost)
            
            if (i + 1) % 20 == 0:
                print(f"Iteration {i+1}: Cost = {cost:.4f}")
                
        return weights, cost_history
