import pytest
import numpy as np
from qml.hybrid_classical_quantum import HybridModel
from qml.qaoa_solver import QAOASolver

def test_hybrid_model_initialization():
    model = HybridModel()
    assert model.vqe is not None
    assert model.scaler is not None

def test_feature_preprocessing():
    model = HybridModel()
    # Test with 2 features (should pad to 4)
    features = np.array([[0.5, 0.8]])
    processed = model.preprocess_features(features)
    assert processed.shape == (1, 4)
    
    # Test with 5 features (should truncate to 4)
    features_5 = np.array([[0.1, 0.2, 0.3, 0.4, 0.5]])
    processed_5 = model.preprocess_features(features_5)
    assert processed_5.shape == (1, 4)

def test_qaoa_solver_graph():
    solver = QAOASolver()
    edges = [(0, 1), (1, 2)]
    G = solver.build_graph(3, edges)
    
    assert len(G.nodes) == 3
    assert len(G.edges) == 2

# Skip actual training/solving tests in unit testing to save time/compute,
# but we could add mock tests here.
