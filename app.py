import os
import json
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from utils.groq_client import GroqClient
from utils.text_processor import TextProcessor
from utils.image_analyzer import ImageAnalyzer
from utils.audio_processor import AudioProcessor

# Load environment variables
load_dotenv()
app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv("SECRET_KEY", "default-secret-key")

# Initialize components
groq_client = GroqClient(api_key=os.getenv("GROQ_API_KEY"))
text_processor = TextProcessor(groq_client)
image_analyzer = ImageAnalyzer(groq_client)
audio_processor = AudioProcessor(groq_client)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/api/text', methods=['POST'])
def process_text():
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({"error": "No text query provided"}), 400
    
    try:
        response = text_processor.process(query)
        return jsonify({"response": response})
    except Exception as e:
        app.logger.error(f"Error processing text: {str(e)}")
        return jsonify({"error": "Failed to process text query"}), 500

@app.route('/api/image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400
    
    image_file = request.files['image']
    description = request.form.get('description', '')
    
    try:
        analysis = image_analyzer.analyze(image_file, description)
        return jsonify({"analysis": analysis})
    except Exception as e:
        app.logger.error(f"Error analyzing image: {str(e)}")
        return jsonify({"error": "Failed to analyze image"}), 500

@app.route('/api/audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400
    
    audio_file = request.files['audio']
    
    try:
        # Save audio temporarily
        temp_path = "temp_audio.wav"
        audio_file.save(temp_path)
        
        # Process the audio
        text = audio_processor.transcribe(temp_path)
        response = text_processor.process(text)
        
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        return jsonify({
            "transcription": text,
            "response": response
        })
    except Exception as e:
        app.logger.error(f"Error processing audio: {str(e)}")
        return jsonify({"error": "Failed to process audio"}), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html'), 404

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)