import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, MultiHeadAttention, LayerNormalization, Dropout, Add

def build_attention_model(num_features=15):
    """
    Builds a Multi-head self-attention model for tabular health features.
    """
    inputs = Input(shape=(num_features,))
    
    # Reshape for attention layer (batch_size, seq_len, features) -> treat as seq_len=1, features=num_features
    # Or treat each feature as an element in sequence: seq_len=num_features, features=1
    x = tf.expand_dims(inputs, axis=-1) # (batch, 15, 1)
    
    # Linear projection to embedding dimension
    embed_dim = 16
    x = Dense(embed_dim)(x) # (batch, 15, 16)
    
    # Attention block
    attention_output, attention_weights = MultiHeadAttention(
        num_heads=3, 
        key_dim=embed_dim
    )(x, x, return_attention_scores=True)
    
    x = Add()([x, attention_output])
    x = LayerNormalization()(x)
    
    # Flatten and dense
    x = tf.keras.layers.Flatten()(x)
    x = Dense(32, activation='relu')(x)
    x = Dropout(0.2)(x)
    outputs = Dense(1, activation='sigmoid')(x)
    
    # Model returning both predictions and attention weights
    model = Model(inputs=inputs, outputs=[outputs, attention_weights])
    
    # For compiling, we only want to calculate loss on the first output (predictions)
    model.compile(
        optimizer='adam',
        loss=['binary_crossentropy', None], # No loss for attention weights
        metrics=[['accuracy'], []]
    )
    
    return model
