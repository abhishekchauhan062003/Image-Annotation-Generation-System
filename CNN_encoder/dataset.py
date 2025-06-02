import os
import requests
import zipfile
import tarfile
from pathlib import Path
import glob
from tqdm import tqdm
from utils import get_image_stats, print_dataset_info, validate_image_format

class DatasetDownloader:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Flickr8k dataset URLs (alternative sources)
        self.datasets = {
            'flickr8k': {
                'images_url': 'https://github.com/jbrownlee/Datasets/releases/download/Flickr8k/Flickr8k_Dataset.zip',
                'text_url': 'https://github.com/jbrownlee/Datasets/releases/download/Flickr8k/Flickr8k_text.zip',
                'images_dir': 'Flicker8k_Dataset',
                'text_dir': 'Flickr8k_text'
            }
        }
    
    def download_file(self, url, filename):
        """Download a file with progress bar."""
        print(f"Downloading {filename}...")
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            with open(self.data_dir / filename, 'wb') as file:
                with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as pbar:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
                            pbar.update(len(chunk))
            
            print(f"Successfully downloaded {filename}")
            return True
            
        except requests.RequestException as e:
            print(f"Failed to download {filename}: {str(e)}")
            return False
    
    def extract_archive(self, archive_path, extract_to=None):
        """Extract zip or tar archive."""
        if extract_to is None:
            extract_to = self.data_dir
        
        archive_path = Path(archive_path)
        extract_to = Path(extract_to)
        
        print(f"Extracting {archive_path.name}...")
        
        try:
            if archive_path.suffix.lower() == '.zip':
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_to)
            elif archive_path.suffix.lower() in ['.tar', '.gz', '.tgz']:
                with tarfile.open(archive_path, 'r:*') as tar_ref:
                    tar_ref.extractall(extract_to)
            else:
                print(f"Unsupported archive format: {archive_path.suffix}")
                return False
            
            print(f"Successfully extracted {archive_path.name}")
            return True
            
        except Exception as e:
            print(f"Failed to extract {archive_path.name}: {str(e)}")
            return False
    
    def download_flickr8k(self):
        """Download and extract Flickr8k dataset."""
        print("\n" + "="*60)
        print("DOWNLOADING FLICKR8K DATASET")
        print("="*60)
        
        dataset_info = self.datasets['flickr8k']
        
        # Download images
        images_zip = self.data_dir / 'Flickr8k_Dataset.zip'
        if not images_zip.exists():
            if not self.download_file(dataset_info['images_url'], 'Flickr8k_Dataset.zip'):
                return False
        else:
            print(f"Images archive already exists: {images_zip}")
        
        # Download text files
        text_zip = self.data_dir / 'Flickr8k_text.zip'
        if not text_zip.exists():
            if not self.download_file(dataset_info['text_url'], 'Flickr8k_text.zip'):
                return False
        else:
            print(f"Text archive already exists: {text_zip}")
        
        # Extract archives
        if not self.extract_archive(images_zip):
            return False
        if not self.extract_archive(text_zip):
            return False
        
        # Clean up zip files
        try:
            images_zip.unlink()
            text_zip.unlink()
            print("Cleaned up archive files.")
        except:
            print("Could not clean up archive files.")
        
        return True
    
    def create_sample_dataset(self, num_images=1000):
        """Create a smaller sample dataset for testing."""
        print(f"\nCreating sample dataset with {num_images} images...")
        
        # Create sample directory
        sample_dir = self.data_dir / 'sample_images'
        sample_dir.mkdir(exist_ok=True)
        
        # Create some dummy images for testing if no real dataset is available
        import numpy as np
        from PIL import Image
        
        for i in range(num_images):
            # Create a random image
            img_array = np.random.randint(0, 256, (224, 224, 3), dtype=np.uint8)
            img = Image.fromarray(img_array)
            img.save(sample_dir / f'sample_{i:04d}.jpg')
        
        print(f"Created {num_images} sample images in {sample_dir}")
        return sample_dir
    
    def get_image_paths(self, dataset_name='flickr8k'):
        """Get list of all image paths in the dataset."""
        if dataset_name == 'flickr8k':
            # Try to find Flickr8k images
            flickr_dir = self.data_dir / 'Flicker8k_Dataset'
            if flickr_dir.exists():
                image_paths = list(flickr_dir.glob('*.jpg')) + list(flickr_dir.glob('*.jpeg'))
                if image_paths:
                    return [str(path) for path in image_paths]
        
        # Try sample dataset
        sample_dir = self.data_dir / 'sample_images'
        if sample_dir.exists():
            image_paths = list(sample_dir.glob('*.jpg')) + list(sample_dir.glob('*.jpeg'))
            if image_paths:
                return [str(path) for path in image_paths]
        
        # If nothing found, create sample dataset
        print("No dataset found. Creating sample dataset...")
        sample_dir = self.create_sample_dataset()
        image_paths = list(sample_dir.glob('*.jpg'))
        return [str(path) for path in image_paths]

def prepare_dataset():
    """Main function to prepare the dataset."""
    downloader = DatasetDownloader()
    
    # Try to download Flickr8k first
    print("Attempting to download Flickr8k dataset...")
    success = downloader.download_flickr8k()
    
    if not success:
        print("\nFailed to download Flickr8k. Creating sample dataset instead...")
        downloader.create_sample_dataset()
    
    # Get image paths
    image_paths = downloader.get_image_paths()
    
    if not image_paths:
        print("No images found! Creating sample dataset...")
        downloader.create_sample_dataset()
        image_paths = downloader.get_image_paths()
    
    # Filter valid images
    valid_images = [path for path in image_paths if validate_image_format(path)]
    
    print(f"\nFound {len(valid_images)} valid images")
    
    # Print dataset statistics
    if valid_images:
        stats = get_image_stats(valid_images)
        print_dataset_info(stats)
    
    return valid_images

if __name__ == "__main__":
    image_paths = prepare_dataset()
    print(f"Dataset preparation complete. Total images: {len(image_paths)}")
