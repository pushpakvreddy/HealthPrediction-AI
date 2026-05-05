import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense, Dropout

def build_lstm_model(timesteps=50, features=5):
    """
    Builds an LSTM model for Time-Series Analysis.
    Features: 5 vital signs (heart_rate, bp_sys, bp_dia, spo2, temp)
    """
    inputs = Input(shape=(timesteps, features))
    
    # First LSTM layer
    x = LSTM(64, return_sequences=True)(inputs)
    x = Dropout(0.2)(x)
    
    # Second LSTM layer (returning sequences to allow attention if needed later, 
    # but based on prompt "Return sequences and attention weights", we'll just return state or sequence)
    # Actually, we will return sequences from the second LSTM to feed into an attention mechanism or pool.
    # For a pure LSTM returning binary output:
    x = LSTM(64, return_sequences=False)(x)
    x = Dropout(0.2)(x)
    
    # Dense layers
    x = Dense(32, activation='relu')(x)
    outputs = Dense(1, activation='sigmoid')(x) # Binary output (normal/abnormal)
    
    model = Model(inputs=inputs, outputs=outputs)
    
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    return model
