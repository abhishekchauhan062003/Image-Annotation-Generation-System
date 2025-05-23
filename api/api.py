from flask import Flask, request, jsonify

from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import os

import pickle
import numpy as np
from tqdm.notebook import tqdm
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16,preprocess_input
from tensorflow.keras.preprocessing.image import load_img,img_to_array
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model
from tensorflow.keras.utils import to_categorical,plot_model
from tensorflow.keras.layers import Input,Dense,LSTM,Embedding, Dropout,add
from tensorflow.keras.models import load_model
api = Flask(__name__)
CORS(api)

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
vgg_model = VGG16()
# restructure the model
vgg_model = Model(inputs=vgg_model.inputs,
                  outputs=vgg_model.layers[-2].output)
max_length = 35
model = load_model('models/my_model.keras',compile=False)
model.compile(loss='categorical_crossentropy', optimizer='adam')
with open('models/features.pkl', 'rb') as file:
    features = pickle.load(file)
with open('models/tokenizer.pkl', 'rb') as file:
    tokenizer = pickle.load(file)
def idx_to_word(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None
def predict_caption(model, image, tokenizer, max_length):
    # add start tag for generation process
    in_text = 'startseq'
    # iterate over the max length of sequence
    for i in range(max_length):
        # encode input sequence
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        # pad the sequence
        sequence = pad_sequences([sequence], max_length, padding='post')
        # predict next word
        yhat = model.predict([image, sequence], verbose=0)
        # get index with high probability
        yhat = np.argmax(yhat)
        # convert index to word
        word = idx_to_word(yhat, tokenizer)
        # stop if word not found
        if word is None:
            break
        # append word as input for generating next word
        in_text += " " + word
        # stop if we reach end tag
        if word == 'endseq':
            break
    return in_text

def generate_caption(image_path):


    # Placeholder for the actual image captioning model
    # In reality, you would load a model and generate a caption here
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    # reshape data for model
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    # preprocess image from vgg
    image = preprocess_input(image)
    # extract features
    feature = vgg_model.predict(image, verbose=0)
    # predict from the trained model
    text = predict_caption(model, feature, tokenizer, max_length)
    text = text.split(" ")
    text = text[1:-1]
    text = " ".join(text)
    return text

@api.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        caption = generate_caption(file_path)
        os.remove(file_path)
        return jsonify({'caption': caption}), 200
if __name__=="__main__":
    api.run()
