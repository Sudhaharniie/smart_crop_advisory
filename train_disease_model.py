"""
Train Real Plant Disease Detection Model
Using PlantVillage Dataset
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import os

def create_disease_model(num_classes=15):
    """
    Create CNN model for plant disease detection
    """
    model = keras.Sequential([
        # Input layer
        layers.Input(shape=(224, 224, 3)),
        
        # Data augmentation
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
        
        # Convolutional blocks
        layers.Conv2D(32, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.BatchNormalization(),
        
        layers.Conv2D(64, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.BatchNormalization(),
        
        layers.Conv2D(128, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.BatchNormalization(),
        
        layers.Conv2D(256, 3, activation='relu'),
        layers.MaxPooling2D(),
        layers.BatchNormalization(),
        
        # Dense layers
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(512, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train_model_with_dataset(dataset_path):
    """
    Train model with PlantVillage dataset
    
    Dataset structure:
    dataset_path/
        train/
            Healthy/
            Bacterial_Blight/
            Blast/
            ...
        validation/
            Healthy/
            Bacterial_Blight/
            ...
    """
    
    # Data generators
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    # Load data
    train_generator = train_datagen.flow_from_directory(
        os.path.join(dataset_path, 'train'),
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical'
    )
    
    validation_generator = val_datagen.flow_from_directory(
        os.path.join(dataset_path, 'validation'),
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical'
    )
    
    # Create model
    num_classes = len(train_generator.class_indices)
    model = create_disease_model(num_classes)
    
    print(f"Training model with {num_classes} disease classes")
    print(f"Classes: {list(train_generator.class_indices.keys())}")
    
    # Callbacks
    callbacks = [
        keras.callbacks.EarlyStopping(patience=5, restore_best_weights=True),
        keras.callbacks.ReduceLROnPlateau(factor=0.5, patience=3),
        keras.callbacks.ModelCheckpoint(
            'disease_detection_model.h5',
            save_best_only=True,
            monitor='val_accuracy'
        )
    ]
    
    # Train
    history = model.fit(
        train_generator,
        epochs=30,
        validation_data=validation_generator,
        callbacks=callbacks
    )
    
    # Save final model
    model.save('disease_detection_model.h5')
    
    # Save class names
    import json
    with open('disease_classes.json', 'w') as f:
        json.dump(train_generator.class_indices, f)
    
    print(f"Model saved! Final validation accuracy: {max(history.history['val_accuracy']):.2%}")
    
    return model, history

def use_pretrained_model():
    """
    Use pre-trained MobileNetV2 with transfer learning
    Faster training, better accuracy
    """
    
    # Load pre-trained model
    base_model = keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze base model
    base_model.trainable = False
    
    # Add custom layers
    model = keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.5),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(15, activation='softmax')  # 15 disease classes
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

# Example usage:
if __name__ == "__main__":
    print("Plant Disease Detection Model Training")
    print("=" * 50)
    
    # Option 1: Train from scratch
    # dataset_path = "path/to/PlantVillage/dataset"
    # model, history = train_model_with_dataset(dataset_path)
    
    # Option 2: Use pre-trained model (recommended)
    print("\nCreating model with transfer learning...")
    model = use_pretrained_model()
    print("Model created successfully!")
    print("\nTo train this model:")
    print("1. Download PlantVillage dataset from Kaggle")
    print("2. Organize into train/validation folders")
    print("3. Run: train_model_with_dataset('path/to/dataset')")
    
    model.summary()
