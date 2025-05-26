from flask import Flask, request, jsonify
from flask_cors import CORS
from paddleocr import PaddleOCR
import cv2
import numpy as np
import base64
import io
from PIL import Image
import os
import tempfile

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize OCR model (enable angle classification with cls=True)
ocr = PaddleOCR(use_angle_cls=True, lang='en')

def extract_text_from_image(image_data):
    try:
        # Convert base64 to image
        if image_data.startswith('data:image'):
            # Remove the data URL prefix
            image_data = image_data.split(',')[1]
        
        # Decode base64 to bytes
        image_bytes = base64.b64decode(image_data)
        
        # Convert bytes to PIL Image
        pil_image = Image.open(io.BytesIO(image_bytes))
        
        # Convert PIL Image to OpenCV format
        opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        # Run OCR
        result = ocr.ocr(opencv_image, cls=True)

        # Return empty string if result is None or not in expected format
        if not result or not isinstance(result, list):
            return ""

        extracted_text = []

        # Extract text from OCR result
        for line in result:
            if not line:
                continue
            for word_info in line:
                if len(word_info) >= 2 and len(word_info[1]) >= 1:
                    text = word_info[1][0]  # Extract the text part
                    extracted_text.append(text)

        # Combine and clean up
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
        
        # Extract text from the image
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