from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import os
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

app = Flask(__name__)
CORS(app)

# Local model paths (absolute path recommended)
MODEL_PATH = os.path.abspath("models/blip-image-captioning-base")

# Check if all required files exist
REQUIRED_FILES = [
    "config.json",
    "preprocessor_config.json",
    "pytorch_model.bin",
    "tokenizer_config.json",
    "vocab.txt",
    "special_tokens_map.json"
]

for file in REQUIRED_FILES:
    if not os.path.isfile(os.path.join(MODEL_PATH, file)):
        raise FileNotFoundError(f"Missing required file: {file}")

# Initialize model from local files
device = "cuda" if torch.cuda.is_available() else "cpu"
processor = BlipProcessor.from_pretrained(MODEL_PATH)
model = BlipForConditionalGeneration.from_pretrained(MODEL_PATH).to(device)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    file_path = os.path.join('uploads', file.filename)
    try:
        file.save(file_path)
        image = Image.open(file_path).convert('RGB')
        
        # Generate caption
        inputs = processor(image, return_tensors="pt").to(device)
        outputs = model.generate(**inputs)
        caption = processor.decode(outputs[0], skip_special_tokens=True)
        
        return jsonify({'caption': caption}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == "__main__":
    os.makedirs('uploads', exist_ok=True)
    app.run()