import os
import json
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard
from models.cnn_model import build_cnn_model
from models.lstm_model import build_lstm_model
from models.attention_model import build_attention_model
from image_preprocessing import get_data_generators, calculate_class_weights
import matplotlib.pyplot as plt

def save_history(history, filename):
    with open(filename, 'w') as f:
        # history.history contains numpy types sometimes, so convert to float
        hist_dict = {k: [float(val) for val in v] for k, v in history.history.items()}
        json.dump(hist_dict, f, indent=4)

def plot_history(history, title, filepath):
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='train')
    if 'val_accuracy' in history.history:
        plt.plot(history.history['val_accuracy'], label='val')
    plt.title(f'{title} Accuracy')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='train')
    if 'val_loss' in history.history:
        plt.plot(history.history['val_loss'], label='val')
    plt.title(f'{title} Loss')
    plt.legend()
    
    plt.savefig(filepath)
    plt.close()

def train_cnn(data_dir: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    
    train_gen, val_gen, _ = get_data_generators(data_dir)
    
    if train_gen is None:
        print("Training data for CNN not found. Skipping.")
        return
        
    class_weights = calculate_class_weights(train_gen)
    
    model = build_cnn_model(num_classes=train_gen.num_classes)
    
    callbacks = [
        EarlyStopping(patience=5, restore_best_weights=True),
        ModelCheckpoint(os.path.join(output_dir, 'cnn_best.keras'), save_best_only=True),
        TensorBoard(log_dir=os.path.join(output_dir, 'logs/cnn'))
    ]
    
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=20,
        class_weight=class_weights,
        callbacks=callbacks
    )
    
    save_history(history, os.path.join(output_dir, 'cnn_history.json'))
    plot_history(history, "CNN Model", os.path.join(output_dir, 'cnn_curves.png'))
    model.save(os.path.join(output_dir, 'cnn_final.keras'))

def train_lstm(X_train, y_train, X_val, y_val, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    
    model = build_lstm_model(timesteps=X_train.shape[1], features=X_train.shape[2])
    
    callbacks = [
        EarlyStopping(patience=5, restore_best_weights=True),
        ModelCheckpoint(os.path.join(output_dir, 'lstm_best.keras'), save_best_only=True),
        TensorBoard(log_dir=os.path.join(output_dir, 'logs/lstm'))
    ]
    
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=50,
        batch_size=32,
        callbacks=callbacks
    )
    
    save_history(history, os.path.join(output_dir, 'lstm_history.json'))
    plot_history(history, "LSTM Model", os.path.join(output_dir, 'lstm_curves.png'))
    model.save(os.path.join(output_dir, 'lstm_final.keras'))

def train_attention(X_train, y_train, X_val, y_val, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    
    model = build_attention_model(num_features=X_train.shape[1])
    
    callbacks = [
        EarlyStopping(patience=5, restore_best_weights=True),
        ModelCheckpoint(os.path.join(output_dir, 'attention_best.keras'), save_best_only=True),
        TensorBoard(log_dir=os.path.join(output_dir, 'logs/attention'))
    ]
    
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=50,
        batch_size=32,
        callbacks=callbacks
    )
    
    save_history(history, os.path.join(output_dir, 'attention_history.json'))
    plot_history(history, "Attention Model", os.path.join(output_dir, 'attention_curves.png'))
    model.save(os.path.join(output_dir, 'attention_final.keras'))

if __name__ == "__main__":
    pass
