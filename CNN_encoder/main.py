"""
Custom Image Encoder for Captioning System
==========================================

This script provides an end-to-end pipeline for:
1. Downloading and preparing image datasets
2. Training a custom CNN encoder from scratch
3. Extracting feature vectors for image captioning

The extracted features can be used with your friend's LSTM decoder.
"""

import os
import sys
import time
import random
from pathlib import Path

# Import our custom modules
from dataset import prepare_dataset
from encoder import train_encoder, CustomImageEncoder
from extract_features import extract_single_image_features, extract_dataset_features, demonstrate_feature_extraction
from utils import create_directories, print_dataset_info

def setup_environment():
    """Setup the project environment and directories."""
    print("🚀 Setting up Custom Image Encoder Project")
    print("="*60)
    
    # Create necessary directories
    create_directories()
    
    # Set random seeds for reproducibility
    import numpy as np
    import tensorflow as tf
    
    seed = 42
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)
    
    print("✅ Environment setup complete!")
    return True

def main_pipeline(
    feature_dim=512,
    epochs=30,
    batch_size=16,
    skip_training=False,
    demo_image_path=None
):
    """
    Main pipeline for the custom image encoder project.
    
    Args:
        feature_dim (int): Dimension of output feature vector
        epochs (int): Number of training epochs
        batch_size (int): Batch size for training
        skip_training (bool): Skip training if model already exists
        demo_image_path (str): Path to demo image for feature extraction
    """
    
    print("\n" + "🎯 CUSTOM IMAGE ENCODER PIPELINE")
    print("="*60)
    print(f"Configuration:")
    print(f"  Feature dimension: {feature_dim}")
    print(f"  Training epochs: {epochs}")
    print(f"  Batch size: {batch_size}")
    print(f"  Skip training: {skip_training}")
    print("="*60)
    
    try:
        # Step 1: Setup environment
        print("\n📁 Step 1: Setting up environment...")
        setup_environment()
        
        # Step 2: Prepare dataset
        print("\n📊 Step 2: Preparing dataset...")
        image_paths = prepare_dataset()
        
        if not image_paths:
            print("❌ No images found! Cannot proceed.")
            return False
        
        print(f"✅ Dataset ready with {len(image_paths)} images")
        
        # Step 3: Train encoder (or skip if requested)
        model_path = 'models/custom_encoder_feature_extractor.keras'
        
        if skip_training and Path(model_path).exists():
            print(f"\n⏭️  Step 3: Skipping training (model exists at {model_path})")
        else:
            print(f"\n🧠 Step 3: Training custom CNN encoder...")
            start_time = time.time()
            
            # Train the encoder
            encoder = train_encoder(
                image_paths=image_paths,
                feature_dim=feature_dim,
                epochs=epochs,
                batch_size=batch_size
            )
            
            training_time = time.time() - start_time
            print(f"✅ Training completed in {training_time/60:.1f} minutes")
        
        # Step 4: Verify model exists
        if not Path(model_path).exists():
            print(f"❌ Model not found at {model_path}")
            return False
        
        # Step 5: Extract features from sample images
        print(f"\n🔍 Step 4: Extracting features from sample images...")
        
        # Select a few sample images for feature extraction
        sample_images = image_paths[:min(10, len(image_paths))]
        
        sample_features = extract_dataset_features(
            image_paths=sample_images,
            model_path=model_path,
            output_path='outputs/sample_features.json',
            batch_size=min(batch_size, len(sample_images))
        )
        
        if sample_features:
            print(f"✅ Extracted features from {len(sample_features)} sample images")
        
        # Step 6: Demonstrate feature extraction on a single image
        print(f"\n🎪 Step 5: Demonstrating feature extraction...")
        
        # Use provided demo image or select a random one
        if demo_image_path and Path(demo_image_path).exists():
            test_image = demo_image_path
        else:
            test_image = random.choice(image_paths)
        
        demo_features = demonstrate_feature_extraction(
            test_image_path=test_image,
            model_path=model_path
        )
        
        # Step 7: Final summary
        print(f"\n🎉 PIPELINE COMPLETED SUCCESSFULLY!")
        print("="*60)
        print("📋 Summary:")
        print(f"  ✅ Dataset: {len(image_paths)} images processed")
        print(f"  ✅ Model: Custom CNN encoder trained")
        print(f"  ✅ Feature dimension: {feature_dim}")
        print(f"  ✅ Sample features extracted: {len(sample_features) if sample_features else 0}")
        print(f"  ✅ Demo image processed: {Path(test_image).name}")
        
        if demo_features is not None:
            print(f"  ✅ Demo feature shape: {demo_features.shape}")
            print(f"  ✅ Feature ready for LSTM decoder! 🚀")
        
        print("\n📁 Output files:")
        print(f"  🔧 Trained model: models/custom_encoder_feature_extractor.keras")
        print(f"  📊 Sample features: outputs/sample_features.json")
        print(f"  🎯 Demo features: outputs/demo_features.json")
        print(f"  📈 Training history: outputs/training_history.png")
        
        print("\n🔗 Next steps:")
        print("  1. Share the trained model with your friend")
        print("  2. Use extract_features.py to extract features from new images")
        print("  3. Feed the feature vectors to the LSTM decoder")
        print("  4. Generate amazing image captions! ✨")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Pipeline failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def quick_demo():
    """Run a quick demonstration with minimal training."""
    print("🚀 Running Quick Demo Mode")
    print("This will use a small dataset and minimal training for demonstration.")
    
    return main_pipeline(
        feature_dim=256,  # Smaller feature dimension
        epochs=5,         # Few epochs for quick demo
        batch_size=8,     # Small batch size
        skip_training=False
    )

def production_run():
    """Run the full production pipeline."""
    print("🏭 Running Production Mode")
    print("This will use full training parameters for best results.")
    
    return main_pipeline(
        feature_dim=512,  # Full feature dimension
        epochs=50,        # More epochs for better training
        batch_size=32,    # Larger batch size
        skip_training=False
    )

def extract_only_mode(image_path=None):
    """Run only feature extraction (assumes model is already trained)."""
    print("🔍 Running Extract-Only Mode")
    
    if image_path:
        # Extract from specific image
        features = extract_single_image_features(image_path)
        return features is not None
    else:
        # Extract from dataset
        image_paths = prepare_dataset()
        features = extract_dataset_features(image_paths)
        return len(features) > 0

if __name__ == "__main__":
    print("""
    🎨 Custom Image Encoder for Captioning System
    ============================================
    
    This tool creates a custom CNN encoder from scratch for image captioning.
    The extracted features can be used with your friend's LSTM decoder.
    """)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == "demo":
            success = quick_demo()
        elif mode == "production":
            success = production_run()
        elif mode == "extract":
            image_path = sys.argv[2] if len(sys.argv) > 2 else None
            success = extract_only_mode(image_path)
        else:
            print(f"Unknown mode: {mode}")
            print("Available modes: demo, production, extract")
            success = False
    else:
        # Interactive mode
        print("\nSelect mode:")
        print("1. Quick Demo (5 epochs, small dataset)")
        print("2. Full Production Run (50 epochs, full training)")
        print("3. Extract Features Only (skip training)")
        print("4. Custom Configuration")
        
        try:
            choice = input("\nEnter choice (1-4): ").strip()
            
            if choice == "1":
                success = quick_demo()
            elif choice == "2":
                success = production_run()
            elif choice == "3":
                success = extract_only_mode()
            elif choice == "4":
                print("\nCustom Configuration:")
                feature_dim = int(input("Feature dimension (default 512): ") or "512")
                epochs = int(input("Training epochs (default 30): ") or "30")
                batch_size = int(input("Batch size (default 16): ") or "16")
                
                success = main_pipeline(
                    feature_dim=feature_dim,
                    epochs=epochs,
                    batch_size=batch_size
                )
            else:
                print("Invalid choice. Running quick demo...")
                success = quick_demo()
                
        except KeyboardInterrupt:
            print("\n\n👋 Operation cancelled by user.")
            success = False
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            success = False
    
    # Final status
    if success:
        print("\n🎉 All done! Your custom image encoder is ready! 🚀")
        print("Check the outputs/ directory for extracted features.")
    else:
        print("\n😞 Something went wrong. Check the error messages above.")
    
    print("\n" + "="*60)
