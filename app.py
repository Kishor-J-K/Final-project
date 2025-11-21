# app.py
from flask import Flask, request, render_template, jsonify
import os
import torch
from torchvision import models
import torch.nn as nn
from src.inference import predict_class
import base64
import uuid
from datetime import datetime

app = Flask(__name__)

# --- Model Setup ---
# Define the number of classes (should match your labels.json)
NUM_CLASSES = 23

# Build the model architecture
model = models.resnet50(pretrained=False) # The warning about 'pretrained' is expected and can be ignored.
model.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False) #
model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES) #

# Load the trained model weights
# Use a relative path for better portability
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model', 'sound_model.pth')
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
model.eval()

# --- App Routes ---

@app.route('/')
def index():
    # Renders the main page with an empty result
    return render_template('index.html', result="")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('index.html', result="No file part in request.")
    
    file = request.files['file']
    
    if file.filename == '':
        return render_template('index.html', result="No file selected.")
    
    if file:
        # Ensure the uploads directory exists
        uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        
        # Save the uploaded file temporarily
        file_path = os.path.join(uploads_dir, file.filename)
        file.save(file_path)
        
        # Predict the class of the uploaded audio file
        predicted_class = predict_class(file_path, model)
        
        # Clean up the class name (replace underscores with spaces)
        display_result = f"Predicted Species: {predicted_class.replace('_', ' ')}"
        
        # Render the page again with the prediction result
        return render_template('index.html', result=display_result)

@app.route('/record', methods=['POST'])
def record_audio():
    try:
        # Get audio data from request (base64 encoded)
        data = request.get_json()
        if not data or 'audio' not in data:
            return jsonify({'error': 'No audio data received'}), 400
        
        audio_data = data['audio']
        
        # Determine file extension from mime type
        # JavaScript now converts to WAV, so default to .wav
        file_ext = '.wav'
        if 'audio/wav' in audio_data or 'audio/wave' in audio_data:
            file_ext = '.wav'
        elif 'audio/webm' in audio_data:
            # Fallback: if WebM is received, we'll try to handle it
            file_ext = '.webm'
        elif 'audio/ogg' in audio_data:
            file_ext = '.ogg'
        elif 'audio/mp4' in audio_data:
            file_ext = '.m4a'
        
        # Remove data URL prefix if present (data:audio/wav;base64,)
        if ',' in audio_data:
            audio_data = audio_data.split(',')[1]
        
        # Decode base64 audio data
        audio_bytes = base64.b64decode(audio_data)
        
        # Ensure the uploads directory exists
        uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = uuid.uuid4().hex[:8]
        filename = f'recording_{timestamp}_{unique_id}{file_ext}'
        file_path = os.path.join(uploads_dir, filename)
        
        # Save the audio file
        with open(file_path, 'wb') as f:
            f.write(audio_bytes)
        
        # If WebM was received (fallback), try to convert it
        if file_ext == '.webm':
            try:
                from pydub import AudioSegment
                audio = AudioSegment.from_file(file_path, format="webm")
                wav_path = os.path.join(uploads_dir, f'recording_{timestamp}_{unique_id}.wav')
                audio.export(wav_path, format="wav")
                file_path = wav_path
            except Exception as conv_error:
                # If conversion fails, try librosa directly (may work if ffmpeg is available)
                print(f"Warning: WebM to WAV conversion failed: {conv_error}")
                print("Attempting to use librosa directly (requires ffmpeg)...")
        
        # Predict the class of the recorded audio file
        predicted_class = predict_class(file_path, model)
        
        # Clean up the class name (replace underscores with spaces)
        display_result = f"Predicted Species: {predicted_class.replace('_', ' ')}"
        
        return jsonify({'success': True, 'prediction': display_result})
    
    except Exception as e:
        import traceback
        error_msg = f"{str(e)}\n{traceback.format_exc()}"
        return jsonify({'error': error_msg}), 500

if __name__ == '__main__':
    # Use environment variable for port (required by hosting platforms like Heroku, Railway, Render)
    port = int(os.environ.get('PORT', 5000))
    # Only enable debug mode in development
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)