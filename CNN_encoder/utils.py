import numpy as np
import cv2
from tensorflow.keras.applications.imagenet_utils import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
import os

def preprocess_image(image_path, target_size=(224, 224)):
    """
    Load and preprocess an image for the CNN encoder.
    
    Args:
        image_path (str): Path to the image file
        target_size (tuple): Target dimensions for resizing
    
    Returns:
        np.ndarray: Preprocessed image array
    """
    try:
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image from {image_path}")
        
        # Convert BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize image
        image = cv2.resize(image, target_size)
        
        # Convert to array and expand dimensions
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)
        
        # Normalize pixel values to [0, 1]
        image = image.astype('float32') / 255.0
        
        return image
    
    except Exception as e:
        print(f"Error preprocessing image {image_path}: {str(e)}")
        return None

def batch_preprocess_images(image_paths, target_size=(224, 224), batch_size=32):
    """
    Preprocess multiple images in batches.
    
    Args:
        image_paths (list): List of image file paths
        target_size (tuple): Target dimensions for resizing
        batch_size (int): Number of images to process at once
    
    Yields:
        np.ndarray: Batch of preprocessed images
    """
    for i in range(0, len(image_paths), batch_size):
        batch_paths = image_paths[i:i + batch_size]
        batch_images = []
        
        for path in batch_paths:
            img = preprocess_image(path, target_size)
            if img is not None:
                batch_images.append(img[0])  # Remove the extra dimension added by preprocess_image
        
        if batch_images:
            yield np.array(batch_images)

def create_directories():
    """Create necessary directories for the project."""
    directories = ['data', 'models', 'outputs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def validate_image_format(image_path):
    """
    Validate if the image file is in a supported format.
    
    Args:
        image_path (str): Path to the image file
    
    Returns:
        bool: True if valid, False otherwise
    """
    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    _, ext = os.path.splitext(image_path.lower())
    return ext in valid_extensions

def get_image_stats(image_paths):
    """
    Get basic statistics about the image dataset.
    
    Args:
        image_paths (list): List of image file paths
    
    Returns:
        dict: Dictionary containing dataset statistics
    """
    total_images = len(image_paths)
    valid_images = sum(1 for path in image_paths if validate_image_format(path))
    
    # Sample a few images to get dimension statistics
    sample_size = min(100, total_images)
    dimensions = []
    
    for i in range(0, sample_size):
        try:
            img = cv2.imread(image_paths[i])
            if img is not None:
                dimensions.append(img.shape[:2])  # (height, width)
        except:
            continue
    
    if dimensions:
        heights, widths = zip(*dimensions)
        avg_height = np.mean(heights)
        avg_width = np.mean(widths)
        min_height, max_height = min(heights), max(heights)
        min_width, max_width = min(widths), max(widths)
    else:
        avg_height = avg_width = 0
        min_height = max_height = min_width = max_width = 0
    
    return {
        'total_images': total_images,
        'valid_images': valid_images,
        'avg_dimensions': (avg_height, avg_width),
        'min_dimensions': (min_height, min_width),
        'max_dimensions': (max_height, max_width),
        'sample_size': len(dimensions)
    }

def print_dataset_info(stats):
    """Print formatted dataset information."""
    print("\n" + "="*50)
    print("DATASET INFORMATION")
    print("="*50)
    print(f"Total images found: {stats['total_images']}")
    print(f"Valid image formats: {stats['valid_images']}")
    print(f"Average dimensions: {stats['avg_dimensions'][0]:.1f} x {stats['avg_dimensions'][1]:.1f}")
    print(f"Min dimensions: {stats['min_dimensions'][0]} x {stats['min_dimensions'][1]}")
    print(f"Max dimensions: {stats['max_dimensions'][0]} x {stats['max_dimensions'][1]}")
    print(f"Statistics based on {stats['sample_size']} samples")
    print("="*50 + "\n")
