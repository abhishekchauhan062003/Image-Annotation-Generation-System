import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, callbacks
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from utils import batch_preprocess_images
from sklearn.model_selection import train_test_split

class CustomImageEncoder:
    def __init__(self, input_shape=(224, 224, 3), feature_dim=512):
        """
        Initialize custom CNN encoder for image feature extraction.
        
        Args:
            input_shape (tuple): Input image dimensions
            feature_dim (int): Dimension of output feature vector
        """
        self.input_shape = input_shape
        self.feature_dim = feature_dim
        self.model = None
        self.history = None
        
    def build_encoder(self):
        """Build the custom CNN encoder architecture."""
        
        model = models.Sequential([
            # First Convolutional Block
            layers.Conv2D(64, (3, 3), activation='relu', padding='same', 
                         input_shape=self.input_shape, name='conv1_1'),
            layers.Conv2D(64, (3, 3), activation='relu', padding='same', name='conv1_2'),
            layers.MaxPooling2D((2, 2), name='pool1'),
            layers.BatchNormalization(name='bn1'),
            
            # Second Convolutional Block
            layers.Conv2D(128, (3, 3), activation='relu', padding='same', name='conv2_1'),
            layers.Conv2D(128, (3, 3), activation='relu', padding='same', name='conv2_2'),
            layers.MaxPooling2D((2, 2), name='pool2'),
            layers.BatchNormalization(name='bn2'),
            
            # Third Convolutional Block
            layers.Conv2D(256, (3, 3), activation='relu', padding='same', name='conv3_1'),
            layers.Conv2D(256, (3, 3), activation='relu', padding='same', name='conv3_2'),
            layers.Conv2D(256, (3, 3), activation='relu', padding='same', name='conv3_3'),
            layers.MaxPooling2D((2, 2), name='pool3'),
            layers.BatchNormalization(name='bn3'),
            
            # Fourth Convolutional Block
            layers.Conv2D(512, (3, 3), activation='relu', padding='same', name='conv4_1'),
            layers.Conv2D(512, (3, 3), activation='relu', padding='same', name='conv4_2'),
            layers.Conv2D(512, (3, 3), activation='relu', padding='same', name='conv4_3'),
            layers.MaxPooling2D((2, 2), name='pool4'),
            layers.BatchNormalization(name='bn4'),
            
            # Fifth Convolutional Block
            layers.Conv2D(512, (3, 3), activation='relu', padding='same', name='conv5_1'),
            layers.Conv2D(512, (3, 3), activation='relu', padding='same', name='conv5_2'),
            layers.Conv2D(512, (3, 3), activation='relu', padding='same', name='conv5_3'),
            layers.MaxPooling2D((2, 2), name='pool5'),
            layers.BatchNormalization(name='bn5'),
            
            # Global Average Pooling instead of Flatten to reduce parameters
            layers.GlobalAveragePooling2D(name='global_avg_pool'),
            
            # Feature extraction layers
            layers.Dense(1024, activation='relu', name='fc1'),
            layers.Dropout(0.5, name='dropout1'),
            layers.Dense(self.feature_dim, activation='relu', name='feature_vector'),
            layers.Dropout(0.3, name='dropout2'),
            
            # Output layer for reconstruction task (unsupervised learning)
            layers.Dense(1024, activation='relu', name='decoder_1'),
            layers.Dense(np.prod(self.input_shape), activation='sigmoid', name='reconstruction')
        ])
        
        self.model = model
        return model
    
    def ensure_model_built(self):
        """Ensure the model is built with proper input shape."""
        if self.model is None:
            self.build_encoder()
        
        if not self.model.built:
            # Build the model with explicit input shape
            self.model.build(input_shape=(None,) + self.input_shape)
            print(f"Model built with input shape: {(None,) + self.input_shape}")
    
    def build_feature_extractor(self):
        """Build feature extractor model (encoder only, without reconstruction)."""
        # Ensure model is built first
        self.ensure_model_built()
        
        # Create feature extractor model up to the feature vector layer
        feature_extractor = models.Model(
            inputs=self.model.input,
            outputs=self.model.get_layer('feature_vector').output,
            name='feature_extractor'
        )
        
        return feature_extractor
    
    def compile_model(self, learning_rate=0.001):
        """Compile the model with appropriate loss and optimizer."""
        if self.model is None:
            self.build_encoder()
        
        # Ensure model is built before compiling
        self.ensure_model_built()
        
        optimizer = optimizers.Adam(learning_rate=learning_rate)
        
        # Using reconstruction loss (MSE) for unsupervised learning
        self.model.compile(
            optimizer=optimizer,
            loss='mse',  # Mean Squared Error for reconstruction
            metrics=['mae']  # Mean Absolute Error as additional metric
        )
        
        print("Model compiled successfully!")
        self.model.summary()
    
    def create_data_generator(self, image_paths, batch_size=32, shuffle=True):
        """Create a data generator for training."""
        def data_generator():
            while True:
                if shuffle:
                    np.random.shuffle(image_paths)
                
                for batch_images in batch_preprocess_images(image_paths, 
                                                           target_size=self.input_shape[:2], 
                                                           batch_size=batch_size):
                    # For autoencoder training, input and target are the same
                    # Flatten the images for reconstruction target
                    batch_flat = batch_images.reshape(batch_images.shape[0], -1)
                    yield batch_images, batch_flat
        
        return data_generator()
    
    def train(self, image_paths, epochs=50, batch_size=32, validation_split=0.2):
        """
        Train the encoder using reconstruction loss (autoencoder approach).
        
        Args:
            image_paths (list): List of image file paths
            epochs (int): Number of training epochs
            batch_size (int): Batch size for training
            validation_split (float): Fraction of data to use for validation
        """
        if self.model is None:
            self.compile_model()
        
        print(f"\nStarting training on {len(image_paths)} images...")
        print(f"Epochs: {epochs}, Batch size: {batch_size}")
        print("="*60)
        
        # Split data into train and validation
        train_paths, val_paths = train_test_split(
            image_paths, test_size=validation_split, random_state=42
        )
        
        print(f"Training images: {len(train_paths)}")
        print(f"Validation images: {len(val_paths)}")
        
        # Create data generators
        train_gen = self.create_data_generator(train_paths, batch_size, shuffle=True)
        val_gen = self.create_data_generator(val_paths, batch_size, shuffle=False)
        
        # Calculate steps per epoch
        steps_per_epoch = max(1, len(train_paths) // batch_size)
        validation_steps = max(1, len(val_paths) // batch_size)
        
        print(f"Steps per epoch: {steps_per_epoch}")
        print(f"Validation steps: {validation_steps}")
        
        # Create models directory for checkpoints
        Path('models').mkdir(exist_ok=True)
        
        # Callbacks
        callbacks_list = [
            callbacks.EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True,
                verbose=1
            ),
            callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7,
                verbose=1
            ),
            callbacks.ModelCheckpoint(
                'models/best_encoder.keras',
                monitor='val_loss',
                save_best_only=True,
                verbose=1
            )
        ]
        
        # Train the model
        try:
            self.history = self.model.fit(
                train_gen,
                steps_per_epoch=steps_per_epoch,
                epochs=epochs,
                validation_data=val_gen,
                validation_steps=validation_steps,
                callbacks=callbacks_list,
                verbose=1
            )
            
            print("\nTraining completed successfully!")
        except Exception as e:
            print(f"Training failed with error: {str(e)}")
            # Try to build model with dummy data if training fails
            print("Attempting to build model with dummy data...")
            dummy_input = tf.random.normal((1,) + self.input_shape)
            dummy_output = self.model(dummy_input)
            print(f"Model successfully built with dummy data. Output shape: {dummy_output.shape}")
        
        return self.history
    
    def plot_training_history(self, save_path='outputs/training_history.png'):
        """Plot training history."""
        if self.history is None:
            print("No training history available.")
            return
        
        # Create outputs directory
        Path(save_path).parent.mkdir(exist_ok=True)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Plot loss
        ax1.plot(self.history.history['loss'], label='Training Loss')
        ax1.plot(self.history.history['val_loss'], label='Validation Loss')
        ax1.set_title('Model Loss')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Loss')
        ax1.legend()
        ax1.grid(True)
        
        # Plot MAE
        ax2.plot(self.history.history['mae'], label='Training MAE')
        ax2.plot(self.history.history['val_mae'], label='Validation MAE')
        ax2.set_title('Model MAE')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('MAE')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"Training history saved to {save_path}")
    
    def save_model(self, filepath='models/custom_encoder.keras'):
        """Save the trained model."""
        if self.model is None:
            print("No model to save.")
            return
        
        # Create models directory
        Path(filepath).parent.mkdir(exist_ok=True)
        
        try:
            # Save full model
            self.model.save(filepath)
            print(f"Full model saved: {filepath}")
            
            # Try to save feature extractor separately (only if model input is accessible)
            try:
                self.ensure_model_built()
                feature_extractor = self.build_feature_extractor()
                feature_extractor_path = filepath.replace('.keras', '_feature_extractor.keras')
                feature_extractor.save(feature_extractor_path)
                print(f"Feature extractor saved: {feature_extractor_path}")
            except Exception as fe_error:
                print(f"Could not save feature extractor: {str(fe_error)}")
                print("You can extract features using the full model later.")
            
            print("Models saved successfully!")
            
        except Exception as e:
            print(f"Error saving full model: {str(e)}")
            print("Attempting alternative save method...")
            
            # Alternative: Save weights only (fix the filename format)
            weights_path = filepath.replace('.keras', '.weights.h5')
            try:
                self.model.save_weights(weights_path)
                print(f"Model weights saved: {weights_path}")
            except Exception as w_error:
                print(f"Could not save weights: {str(w_error)}")
                print("Model saving failed completely.")
    
    def load_model(self, filepath='models/custom_encoder.keras'):
        """Load a trained model."""
        try:
            self.model = tf.keras.models.load_model(filepath)
            print(f"Model loaded from {filepath}")
            return True
        except Exception as e:
            print(f"Failed to load model: {str(e)}")
            return False

def train_encoder(image_paths, feature_dim=512, epochs=50, batch_size=32):
    """
    Main function to train the custom encoder.
    
    Args:
        image_paths (list): List of image file paths
        feature_dim (int): Dimension of feature vector
        epochs (int): Number of training epochs
        batch_size (int): Batch size
    
    Returns:
        CustomImageEncoder: Trained encoder instance
    """
    print("\n" + "="*60)
    print("TRAINING CUSTOM IMAGE ENCODER")
    print("="*60)
    
    # Initialize encoder
    encoder = CustomImageEncoder(feature_dim=feature_dim)
    
    # Build and compile model
    encoder.compile_model()
    
    # Train the model
    history = encoder.train(
        image_paths=image_paths,
        epochs=epochs,
        batch_size=batch_size
    )
    
    # Plot training history
    # encoder.plot_training_history()
    
    # Save the model
    encoder.save_model()
    
    print("\nEncoder training completed successfully!")
    return encoder

if __name__ == "__main__":
    # This would be called from main.py
    print("CustomImageEncoder module loaded.")