import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def get_data_generators(data_dir: str, target_size=(224, 224), batch_size=32):
    """
    Creates train/val/test data generators with augmentation for training.
    """
    # Assuming data_dir has train, val, test subdirectories
    train_dir = os.path.join(data_dir, 'train')
    val_dir = os.path.join(data_dir, 'val')
    test_dir = os.path.join(data_dir, 'test')
    
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        zoom_range=0.15,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    # Only rescale for validation and testing
    val_test_datagen = ImageDataGenerator(rescale=1./255)
    
    train_generator = None
    if os.path.exists(train_dir):
        train_generator = train_datagen.flow_from_directory(
            train_dir,
            target_size=target_size,
            batch_size=batch_size,
            class_mode='categorical'
        )
        
    val_generator = None
    if os.path.exists(val_dir):
        val_generator = val_test_datagen.flow_from_directory(
            val_dir,
            target_size=target_size,
            batch_size=batch_size,
            class_mode='categorical'
        )
        
    test_generator = None
    if os.path.exists(test_dir):
        test_generator = val_test_datagen.flow_from_directory(
            test_dir,
            target_size=target_size,
            batch_size=batch_size,
            class_mode='categorical',
            shuffle=False
        )
        
    return train_generator, val_generator, test_generator

def calculate_class_weights(generator):
    """Calculates class weights to handle imbalance."""
    from sklearn.utils.class_weight import compute_class_weight
    import numpy as np
    
    if generator is None:
        return None
        
    classes = generator.classes
    class_weights = compute_class_weight(
        class_weight='balanced',
        classes=np.unique(classes),
        y=classes
    )
    
    return dict(enumerate(class_weights))
