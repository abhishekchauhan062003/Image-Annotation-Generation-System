# utils/image_utils.py

import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from config import IMAGE_SIZE

def preprocess_image(img_path):
    img = load_img(img_path, target_size=IMAGE_SIZE)
    img = img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    return tf.convert_to_tensor(img, dtype=tf.float32)
