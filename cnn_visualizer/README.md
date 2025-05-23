# CNN Visualizer

This project implements a custom CNN from scratch in TensorFlow using low-level operations. It also visualizes intermediate feature maps after each convolution and pooling layer.

## Structure
- `model/cnn_model.py`: Custom CNN model implemented with tf.nn operations.
- `utils/image_utils.py`: Image loading and preprocessing utilities.
- `utils/visualizer.py`: Visualization of feature maps with matplotlib.
- `assets/`: Contains sample images for testing.
- `main.py`: Entry point to run the visualization on a sample image.
- `config.py`: Configuration file for image paths and parameters.

## Usage

1. Place your image inside the `assets/` folder or update the path in `config.py`.
2. Run:
```bash
python main.py
```
3. You will see feature map visualizations for each conv and pooling layer.

## Requirements
- TensorFlow
- matplotlib
- Pillow
