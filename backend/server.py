from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import io
from PIL import Image
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

OCR_SPACE_API_KEY = 'helloworld'  # Replace with your actual API key for production

def extract_text_from_image(image_data):
    try:
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]

        # Decode base64 image data
        image_bytes = base64.b64decode(image_data)

        # Prepare files and payload for OCR.Space
        files = {'file': ('image.jpg', image_bytes)}
        payload = {
            'apikey': OCR_SPACE_API_KEY,
            'language': 'eng',
            'OCREngine': 2,
            'isOverlayRequired': False
        }

        response = requests.post('https://api.ocr.space/parse/image', files=files, data=payload)

        result = response.json()
        if result.get('IsErroredOnProcessing'):
            return ""

        parsed_results = result.get('ParsedResults')
        if not parsed_results:
            return ""

        extracted_text = parsed_results[0].get('ParsedText', '')
        return extracted_text.strip()

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
