import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array

class DLInference:
    def __init__(self, models_dir: str):
        self.models_dir = models_dir
        
        # Load models if they exist
        cnn_path = os.path.join(models_dir, 'cnn_best.keras')
        self.cnn_model = tf.keras.models.load_model(cnn_path) if os.path.exists(cnn_path) else None
        
        lstm_path = os.path.join(models_dir, 'lstm_best.keras')
        self.lstm_model = tf.keras.models.load_model(lstm_path) if os.path.exists(lstm_path) else None
        
        attention_path = os.path.join(models_dir, 'attention_best.keras')
        # Custom layer might be needed for load_model if we defined any, but we didn't
        self.attention_model = tf.keras.models.load_model(attention_path) if os.path.exists(attention_path) else None

    def predict_image(self, image_path: str, target_size=(224, 224)) -> dict:
        if self.cnn_model is None:
            return {"error": "CNN model not found."}
            
        try:
            img = load_img(image_path, target_size=target_size)
            img_array = img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            
            predictions = self.cnn_model.predict(img_array)
            class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][class_idx])
            
            # Map index to class name later or here if known
            classes = ['Normal', 'Pneumonia', 'Tuberculosis']
            class_name = classes[class_idx] if class_idx < len(classes) else str(class_idx)
            
            return {
                "prediction": class_name,
                "confidence": confidence
            }
        except Exception as e:
            return {"error": str(e)}

    def predict_timeseries(self, sequence_data: np.ndarray) -> dict:
        if self.lstm_model is None:
            return {"error": "LSTM model not found."}
            
        try:
            # sequence_data should be shaped (1, timesteps, features)
            predictions = self.lstm_model.predict(sequence_data)
            prob = float(predictions[0][0])
            
            return {
                "prediction": int(prob > 0.5),
                "probability": prob
            }
        except Exception as e:
            return {"error": str(e)}

    def predict_attention(self, features_data: np.ndarray) -> dict:
        if self.attention_model is None:
            return {"error": "Attention model not found."}
            
        try:
            # features_data should be shaped (1, features)
            outputs, attention_weights = self.attention_model.predict(features_data)
            prob = float(outputs[0][0])
            
            # Extract attention weights for visualization
            # attention_weights shape depends on MultiHeadAttention return, usually (batch, num_heads, seq_len, seq_len)
            # We average across heads for a simpler 1D importance
            avg_attention = np.mean(attention_weights[0], axis=0) # (seq_len, seq_len)
            feature_importance = np.mean(avg_attention, axis=0).tolist()
            
            return {
                "prediction": int(prob > 0.5),
                "probability": prob,
                "attention_weights": feature_importance
            }
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    pass
