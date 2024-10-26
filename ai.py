from flask import Flask, jsonify, request, send_from_directory
from elevenlabs import set_api_key, Voice, VoiceSettings

import cohere
from elevenlabs import Voice, VoiceSettings, generate, set_api_key
import os
import uuid
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import random

app = Flask(__name__)

# Configuration
app.config['AUDIO_FOLDER'] = 'Adam (Legacy)'
app.config['MAX_AUDIO_AGE'] = 3600  # 1 hour in seconds
app.config['COHERE_API_KEY'] = 'zdOo8nXVDqdfHC1BI3CMMb8w9H8X9KER7EA3YJn6'
app.config['ELEVEN_LABS_API_KEY'] = 'sk_1f0bf4cd533a480a16780becfab8c5b4da9fe3731a458c15'

# Initialize API clients
co = cohere.Client(app.config['COHERE_API_KEY'])
set_api_key(app.config['ELEVEN_LABS_API_KEY'])

# Ensure the audio folder exists
if not os.path.exists(app.config['AUDIO_FOLDER']):
    os.makedirs(app.config['AUDIO_FOLDER'])

# Voice settings for ElevenLabs TTS
VOICE_SETTINGS = VoiceSettings(stability=0.71, similarity_boost=0.5, use_speaker_boost=True)

class TransactionProcessor:
    def calculate_environmental_impact(self, amount):
        """Calculate environmental impact metrics."""
        paper_saved = amount * 0.1  # grams of paper
        carbon_saved = paper_saved * 0.9  # grams of CO2
        water_saved = paper_saved * 0.05  # liters of water
        
        return {
            "paper_saved": paper_saved,
            "carbon_saved": carbon_saved,
            "water_saved": water_saved
        }

    def generate_eco_message(self, impact_data):
        """Generate eco-friendly message with Cohere and format it with impact data."""
        prompt = f"Generate a personalized eco-friendly tip based on digital banking that could save {impact_data['carbon_saved']:.1f} grams of CO2."
        
        # Generate response with Cohere
        response = co.generate(
            model='command',
            prompt=prompt,
            max_tokens=50,
            temperature=0.7,
            stop_sequences=["."],
            k=0,
            p=0.7
        )
        
        message = response.generations[0].text.strip() + "."
        return message

    def create_audio_message(self, message, voice_id="pNInz6obpgDQGcFmaJgB"):
        """Convert text to speech using ElevenLabs and save as an audio file."""
        filename = f"eco_message_{uuid.uuid4()}.mp3"
        filepath = os.path.join(app.config['AUDIO_FOLDER'], secure_filename(filename))
        
        audio = generate(
            text=message,
            voice=Voice(
                voice_id=voice_id,
                settings=VOICE_SETTINGS
            ),
            model="eleven_multilingual_v2"
        )
        
        with open(filepath, 'wb') as f:
            f.write(audio)
        
        return filename

processor = TransactionProcessor()

@app.route('/api/transaction', methods=['POST'])
def process_transaction():
    data = request.get_json()
    if not data or 'amount' not in data:
        return jsonify({'status': 'error', 'message': 'Transaction amount is required.'}), 400
    
    amount = float(data['amount'])
    impact_data = processor.calculate_environmental_impact(amount)
    
    # Generate eco message
    eco_message = processor.generate_eco_message(impact_data)
    
    # Convert message to audio
    audio_filename = processor.create_audio_message(eco_message)
    
    return jsonify({
        'status': 'success',
        'data': {
            'eco_message': eco_message,
            'environmental_impact': impact_data,
            'audio_url': f'/api/audio/{audio_filename}'
        }
    })

@app.route('/api/audio/<filename>')
def get_audio(filename):
    """Serve generated audio files."""
    return send_from_directory(app.config['AUDIO_FOLDER'], filename)

@app.route('/api/voices', methods=['GET'])
def get_available_voices():
    """List available voices for ElevenLabs."""
    voices = {
        "pNInz6obpgDQGcFmaJgB": "Adam",
        "21m00Tcm4TlvDq8ikWAM": "Rachel",
        "EXAVITQu4vr4xnSDxMaL": "Bella"
    }
    return jsonify({
        'status': 'success',
        'data': {
            'available_voices': voices
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
