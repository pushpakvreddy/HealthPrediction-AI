import pennylane as qml
from pennylane import numpy as np
import networkx as nx

class QAOASolver:
    def __init__(self, p_layers=3):
        self.p_layers = p_layers

    def build_graph(self, num_treatments, compatibility_edges):
        """
        Builds a compatibility graph of treatments.
        """
        G = nx.Graph()
        G.add_nodes_from(range(num_treatments))
        G.add_edges_from(compatibility_edges)
        return G

    def solve(self, num_treatments, compatibility_edges):
        """
        Solves QAOA for MaxCut problem to select best treatment combinations.
        """
        G = self.build_graph(num_treatments, compatibility_edges)
        dev = qml.device('default.qubit', wires=num_treatments)
        
        # MaxCut Cost Hamiltonian
        cost_h, _ = qml.qaoa.maxcut(G)
        
        # Mixer Hamiltonian
        mixer_h = qml.qaoa.x_mixer(range(num_treatments))
        
        def qaoa_layer(gamma, alpha):
            qml.qaoa.cost_layer(gamma, cost_h)
            qml.qaoa.mixer_layer(alpha, mixer_h)
            
        @qml.qnode(dev)
        def circuit(params, **kwargs):
            # Initial state: equal superposition
            for i in range(num_treatments):
                qml.Hadamard(wires=i)
                
            qml.layer(qaoa_layer, self.p_layers, params[0], params[1])
            return qml.expval(cost_h)
            
        # Optimization
        opt = qml.GradientDescentOptimizer(stepsize=0.1)
        # params[0] are gammas, params[1] are alphas
        params = np.array([[0.1] * self.p_layers, [0.1] * self.p_layers], requires_grad=True)
        
        steps = 50
        for i in range(steps):
            params = opt.step(circuit, params)
            
        # Get final probabilities
        @qml.qnode(dev)
        def probability_circuit(params):
            for i in range(num_treatments):
                qml.Hadamard(wires=i)
            qml.layer(qaoa_layer, self.p_layers, params[0], params[1])
            return qml.probs(wires=range(num_treatments))
            
        probs = probability_circuit(params)
        best_state_index = np.argmax(probs)
        best_state = format(best_state_index, f'0{num_treatments}b')
        
        return best_state, float(probs[best_state_index])
