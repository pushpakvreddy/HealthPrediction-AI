import pennylane as qml
from pennylane import numpy as np

# We'll use 4 qubits for encoding 4 features as specified
n_qubits = 4
dev = qml.device('default.qubit', wires=n_qubits)

@qml.qnode(dev)
def feature_encoding_circuit(features, weights):
    """
    Feature Encoding and Ansatz Circuit.
    features: array of size (n_qubits,)
    weights: array of size (layers, n_qubits, 3) for RX, RY, RZ
    """
    # 1. Feature Encoding Circuit
    # Angle encoding with Hadamard gates first
    for i in range(n_qubits):
        qml.Hadamard(wires=i)
        qml.RX(features[i], wires=i)

    # 2. Ansatz Circuit (Parameterized)
    layers = weights.shape[0]
    for layer in range(layers):
        # Rotation layers: RX, RY, RZ gates
        for i in range(n_qubits):
            qml.RX(weights[layer, i, 0], wires=i)
            qml.RY(weights[layer, i, 1], wires=i)
            qml.RZ(weights[layer, i, 2], wires=i)
        
        # Entangling gates: CNOT between adjacent qubits
        for i in range(n_qubits - 1):
            qml.CNOT(wires=[i, i + 1])
        # Ring topology
        qml.CNOT(wires=[n_qubits - 1, 0])

    # 3. Measurement Circuit
    # Pauli-Z measurement on all qubits
    return [qml.expval(qml.PauliZ(i)) for i in range(n_qubits)]

def get_num_weights(layers):
    return (layers, n_qubits, 3)
