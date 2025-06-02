import tensorflow as tf
import numpy as np
from pathlib import Path
import json
from utils import preprocess_image
from encoder import CustomImageEncoder

class FeatureExtractor:
    def __init__(self, model_path='models/custom_encoder_feature_extractor.keras'):
        """
        Initialize feature extractor with trained model.
        
        Args:
            model_path (str): Path to the trained feature extractor model
        """
        self.model_path = model_path
        self.model = None
        self.feature_dim = None
        self.load_model()
    
    def load_model(self):
        """Load the trained feature extractor model."""
        try:
            if Path(self.model_path).exists():
                self.model = tf.keras.models.load_model(self.model_path)
                self.feature_dim = self.model.output_shape[-1]
                print(f"Feature extractor loaded successfully!")
                print(f"Feature dimension: {self.feature_dim}")
                return True
            else:
                print(f"Model file not found: {self.model_path}")
                return False
        except Exception as e:
            print(f"Failed to load model: {str(e)}")
            return False
    
    def extract_features(self, image_path):
        """
        Extract feature vector from a single image.
        
        Args:
            image_path (str): Path to the image file
        
        Returns:
            np.ndarray: Feature vector of shape (feature_dim,)
        """
        if self.model is None:
            print("Model not loaded. Cannot extract features.")
            return None
        
        try:
            # Preprocess the image
            processed_image = preprocess_image(image_path, target_size=(224, 224))
            
            if processed_image is None:
                print(f"Failed to preprocess image: {image_path}")
                return None
            
            # Extract features
            features = self.model.predict(processed_image, verbose=0)
            
            # Return flattened feature vector
            return features.flatten()
            
        except Exception as e:
            print(f"Error extracting features from {image_path}: {str(e)}")
            return None
    
    def extract_features_batch(self, image_paths, batch_size=32):
        """
        Extract features from multiple images in batches.
        
        Args:
            image_paths (list): List of image file paths
            batch_size (int): Batch size for processing
        
        Returns:
            dict: Dictionary mapping image paths to feature vectors
        """
        if self.model is None:
            print("Model not loaded. Cannot extract features.")
            return {}
        
        features_dict = {}
        
        print(f"Extracting features from {len(image_paths)} images...")
        
        for i in range(0, len(image_paths), batch_size):
            batch_paths = image_paths[i:i + batch_size]
            batch_images = []
            valid_paths = []
            
            # Preprocess batch
            for path in batch_paths:
                processed_img = preprocess_image(path, target_size=(224, 224))
                if processed_img is not None:
                    batch_images.append(processed_img[0])  # Remove batch dimension
                    valid_paths.append(path)
            
            if batch_images:
                # Convert to numpy array
                batch_array = np.array(batch_images)
                
                # Extract features
                batch_features = self.model.predict(batch_array, verbose=0)
                
                # Store features
                for path, features in zip(valid_paths, batch_features):
                    features_dict[path] = features.flatten()
            
            # Progress update
            processed = min(i + batch_size, len(image_paths))
            print(f"Processed {processed}/{len(image_paths)} images")
        
        return features_dict
    
    def save_features(self, features_dict, output_path='outputs/extracted_features.json'):
        """
        Save extracted features to a JSON file.
        
        Args:
            features_dict (dict): Dictionary of image paths to feature vectors
            output_path (str): Path to save the features
        """
        # Convert numpy arrays to lists for JSON serialization
        serializable_features = {}
        for path, features in features_dict.items():
            if isinstance(features, np.ndarray):
                serializable_features[path] = features.tolist()
            else:
                serializable_features[path] = features
        
        # Create output directory
        Path(output_path).parent.mkdir(exist_ok=True)
        
        # Save to JSON
        with open(output_path, 'w') as f:
            json.dump(serializable_features, f, indent=2)
        
        print(f"Features saved to {output_path}")
        print(f"Total features saved: {len(serializable_features)}")
    
    def load_features(self, features_path='outputs/extracted_features.json'):
        """
        Load previously extracted features from JSON file.
        
        Args:
            features_path (str): Path to the features JSON file
        
        Returns:
            dict: Dictionary of image paths to feature vectors
        """
        try:
            with open(features_path, 'r') as f:
                features_dict = json.load(f)
            
            # Convert lists back to numpy arrays
            for path in features_dict:
                features_dict[path] = np.array(features_dict[path])
            
            print(f"Loaded {len(features_dict)} feature vectors from {features_path}")
            return features_dict
            
        except Exception as e:
            print(f"Failed to load features: {str(e)}")
            return {}
    
    def get_feature_statistics(self, features_dict):
        """
        Get statistics about the extracted features.
        
        Args:
            features_dict (dict): Dictionary of image paths to feature vectors
        
        Returns:
            dict: Statistics about the features
        """
        if not features_dict:
            return {}
        
        all_features = np.array(list(features_dict.values()))
        
        stats = {
            'num_images': len(features_dict),
            'feature_dim': all_features.shape[1],
            'mean_values': np.mean(all_features, axis=0).tolist(),
            'std_values': np.std(all_features, axis=0).tolist(),
            'min_values': np.min(all_features, axis=0).tolist(),
            'max_values': np.max(all_features, axis=0).tolist(),
            'overall_mean': float(np.mean(all_features)),
            'overall_std': float(np.std(all_features))
        }
        
        return stats
    
    def print_feature_info(self, features_dict):
        """Print information about extracted features."""
        stats = self.get_feature_statistics(features_dict)
        
        if not stats:
            print("No feature statistics available.")
            return
        
        print("\n" + "="*50)
        print("FEATURE EXTRACTION RESULTS")
        print("="*50)
        print(f"Number of images processed: {stats['num_images']}")
        print(f"Feature vector dimension: {stats['feature_dim']}")
        print(f"Overall feature mean: {stats['overall_mean']:.4f}")
        print(f"Overall feature std: {stats['overall_std']:.4f}")
        print(f"Feature range: [{min(stats['min_values']):.4f}, {max(stats['max_values']):.4f}]")
        print("="*50 + "\n")

def extract_single_image_features(image_path, model_path='models/custom_encoder_feature_extractor.keras'):
    """
    Extract features from a single image (convenience function).
    
    Args:
        image_path (str): Path to the image
        model_path (str): Path to the trained model
    
    Returns:
        np.ndarray: Feature vector
    """
    extractor = FeatureExtractor(model_path)
    features = extractor.extract_features(image_path)
    
    if features is not None:
        print(f"\nFeature extraction successful!")
        print(f"Image: {image_path}")
        print(f"Feature vector shape: {features.shape}")
        print(f"Feature vector (first 10 values): {features[:10]}")
        print(f"Feature statistics - Mean: {np.mean(features):.4f}, Std: {np.std(features):.4f}")
    
    return features

def extract_dataset_features(image_paths, model_path='models/custom_encoder_feature_extractor.keras',
                           output_path='outputs/extracted_features.json', batch_size=32):
    """
    Extract features from a dataset of images.
    
    Args:
        image_paths (list): List of image file paths
        model_path (str): Path to the trained model
        output_path (str): Path to save extracted features
        batch_size (int): Batch size for processing
    
    Returns:
        dict: Dictionary of image paths to feature vectors
    """
    print("\n" + "="*60)
    print("EXTRACTING FEATURES FROM DATASET")
    print("="*60)
    
    extractor = FeatureExtractor(model_path)
    
    if extractor.model is None:
        print("Failed to load model. Cannot extract features.")
        return {}
    
    # Extract features
    features_dict = extractor.extract_features_batch(image_paths, batch_size)
    
    if features_dict:
        # Print feature information
        extractor.print_feature_info(features_dict)
        
        # Save features
        extractor.save_features(features_dict, output_path)
        
        # Save feature statistics
        stats = extractor.get_feature_statistics(features_dict)
        stats_path = output_path.replace('.json', '_stats.json')
        with open(stats_path, 'w') as f:
            json.dump(stats, f, indent=2)
        print(f"Feature statistics saved to {stats_path}")
    
    return features_dict

def demonstrate_feature_extraction(test_image_path, model_path='models/custom_encoder_feature_extractor.keras'):
    """
    Demonstrate feature extraction on a test image with detailed output.
    
    Args:
        test_image_path (str): Path to test image
        model_path (str): Path to trained model
    """
    print("\n" + "="*60)
    print("FEATURE EXTRACTION DEMONSTRATION")
    print("="*60)
    
    extractor = FeatureExtractor(model_path)
    
    if extractor.model is None:
        print("Cannot demonstrate - model not loaded.")
        return
    
    # Extract features
    features = extractor.extract_features(test_image_path)
    
    if features is not None:
        print(f"\n✅ Feature extraction successful!")
        print(f"Image path: {test_image_path}")
        print(f"Feature vector shape: {features.shape}")
        print(f"Feature dimension: {len(features)}")
        
        # Feature statistics
        print(f"\nFeature Statistics:")
        print(f"  Mean: {np.mean(features):.6f}")
        print(f"  Std:  {np.std(features):.6f}")
        print(f"  Min:  {np.min(features):.6f}")
        print(f"  Max:  {np.max(features):.6f}")
        
        # Show first few feature values
        print(f"\nFirst 20 feature values:")
        for i in range(min(20, len(features))):
            print(f"  Feature[{i:2d}]: {features[i]:.6f}")
        
        # Save individual feature vector
        feature_output = {
            'image_path': test_image_path,
            'features': features.tolist(),
            'statistics': {
                'mean': float(np.mean(features)),
                'std': float(np.std(features)),
                'min': float(np.min(features)),
                'max': float(np.max(features))
            }
        }
        
        output_path = 'outputs/demo_features.json'
        Path(output_path).parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(feature_output, f, indent=2)
        
        print(f"\n💾 Demo features saved to: {output_path}")
        print(f"\n🎯 Feature vector ready for LSTM decoder!")
        print("   Shape:", features.shape)
        print("   Type: ", type(features))
        print("   Ready to pass to your friend's LSTM decoder ✨")
        
        return features
    else:
        print("❌ Feature extraction failed!")
        return None

if __name__ == "__main__":
    # Example usage
    print("FeatureExtractor module loaded.")
    print("Use extract_single_image_features() or extract_dataset_features() to extract features.")