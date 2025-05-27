from flask import Flask, request, jsonify
from flask_cors import CORS
import easyocr
import cv2
import numpy as np
import base64
import io
from PIL import Image

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize EasyOCR Reader (lang='en' for English)
reader = easyocr.Reader(['en'], gpu=False)  # Set gpu=True if you have GPU support

def extract_text_from_image(image_data):
    try:
        # Convert base64 to image
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        pil_image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        
        # Convert PIL Image to numpy array (RGB)
        image_np = np.array(pil_image)
        
        # EasyOCR expects RGB, so no need to convert color spaces here
        result = reader.readtext(image_np)

        if not result or not isinstance(result, list):
            return ""

        extracted_text = []

        # result is a list of tuples: (bbox, text, confidence)
        for detection in result:
            text = detection[1]
            extracted_text.append(text)

        clean_text = ' '.join(extracted_text).replace('\n', ' ').strip()
        return clean_text
    
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return ""

@app.route('/api/extract-text', methods=['POST'])
def extract_text():
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        image_data = data['image']
        extracted_text = extract_text_from_image(image_data)
        
        return jsonify({
            'success': True,
            'text': extracted_text
        })
    
    except Exception as e:
        print(f"Error in extract_text endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
