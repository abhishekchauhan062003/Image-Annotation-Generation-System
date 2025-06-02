from config import IMAGE_PATH
from model.cnn_model import VisualCustomCNN
from utils.image_utils import preprocess_image
from utils.visualizer import visualize_feature_maps

def main():
    model = VisualCustomCNN()
    img_tensor = preprocess_image(IMAGE_PATH)
    _, visualizations = model(img_tensor)
    visualize_feature_maps(visualizations)

if __name__ == "__main__":
    main()