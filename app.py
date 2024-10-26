from flask import Flask, jsonify, request, send_from_directory
import cohere
from elevenlabs import generate, save, set_api_key
import os
import random
from datetime import datetime
import uuid
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
app.config['AUDIO_FOLDER'] = 'audio_files'
app.config['MAX_AUDIO_AGE'] = 3600  # 1 hour in seconds
app.config['COHERE_API_KEY'] = 'your-cohere-api-key'
app.config['ELEVEN_LABS_API_KEY'] = 'your-elevenlabs-api-key'

# Initialize API clients
set_api_key(app.config['ELEVEN_LABS_API_KEY'])
co = cohere.Client(app.config['COHERE_API_KEY'])

# Create audio directory if it doesn't exist
if not os.path.exists(app.config['AUDIO_FOLDER']):
    os.makedirs(app.config['AUDIO_FOLDER'])

# Eco-friendly message templates with voice options
ECO_MESSAGES = {
    "digital_banking": [
        {
            "template": "By choosing digital banking, you've saved {paper_saved:.1f} grams of paper, equivalent to saving {trees_saved:.2f} trees annually.",
            "voice": "Antoni"  # Professional, friendly voice
        },
        {
            "template": "Your digital transaction reduced carbon emissions by approximately {carbon_saved:.1f} grams compared to traditional banking.",
            "voice": "Josh"  # Warm, engaging voice
        },
        {
            "template": "This paperless transaction contributes to saving {water_saved:.1f} liters of water used in paper production.",
            "voice": "Rachel"  # Clear, professional voice
        }
    ],
    "energy_tips": [
        {
            "template": "Consider reviewing your transaction history during daylight hours to save energy.",
            "voice": "Bella"  # Friendly, approachable voice
        },
        {
            "template": "Enable dark mode in your banking app to reduce screen energy consumption.",
            "voice": "Sam"  # Informative, clear voice
        }
    ]
}

class TransactionProcessor:
    def __init__(self):
        self.transaction_log = []
    
    def calculate_environmental_impact(self, amount):
        """Calculate environmental impact of digital transaction"""
        paper_saved = amount * 0.1  # grams of paper
        trees_saved = paper_saved * 0.00006  # conversion factor
        carbon_saved = paper_saved * 0.9  # grams of CO2
        water_saved = paper_saved * 0.05  # liters of water
        
        return {
            "paper_saved": paper_saved,
            "trees_saved": trees_saved,
            "carbon_saved": carbon_saved,
            "water_saved": water_saved
        }
    
    def generate_eco_message(self, impact_data):
        """Generate personalized eco-friendly message using Cohere"""
        # Select random message template with voice
        message_data = random.choice(ECO_MESSAGES["digital_banking"])
        message = message_data["template"].format(**impact_data)
        voice = message_data["voice"]
        
        # Generate additional tip using Cohere
        prompt = f"Generate a short eco-friendly tip related to digital banking and environmental impact. Current impact: {message}"
        
        response = co.generate(
            model='command',
            prompt=prompt,
            max_tokens=50,
            temperature=0.7,
            stop_sequences=["."],
            k=0,
            p=0.7
        )
        
        additional_tip = response.generations[0].text.strip() + "."
        final_message = f"{message}\n\nTip: {additional_tip}"
        
        return final_message, voice

    def create_audio_message(self, message, voice):
        """Convert message to speech using ElevenLabs"""
        filename = f"eco_message_{uuid.uuid4()}.mp3"
        filepath = os.path.join(app.config['AUDIO_FOLDER'], secure_filename(filename))
        
        # Generate audio using ElevenLabs
        audio = generate(
            text=message,
            voice=voice,
            model="eleven_monolingual_v1"
        )
        
        # Save the audio file
        save(audio, filepath)
        
        return filename

    def log_transaction(self, transaction_data, eco_message):
        """Log transaction details"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "transaction": transaction_data,
            "eco_message": eco_message
        }
        
        self.transaction_log.append(log_entry)
        
        # Save to file
        with open('transaction_log.json', 'a') as f:
            json.dump(log_entry, f)
            f.write('\n')

processor = TransactionProcessor()

@app.route('/api/transaction', methods=['POST'])
def process_transaction():
    try:
        data = request.get_json()
        
        if not data or 'amount' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Amount is required'
            }), 400
        
        # Calculate environmental impact
        impact = processor.calculate_environmental_impact(float(data['amount']))
        
        # Generate eco message with voice selection
        eco_message, voice = processor.generate_eco_message(impact)
        
        # Create audio file using ElevenLabs
        audio_filename = processor.create_audio_message(eco_message, voice)
        
        # Log transaction
        processor.log_transaction(data, eco_message)
        
        return jsonify({
            'status': 'success',
            'data': {
                'transaction_id': str(uuid.uuid4()),
                'eco_message': eco_message,
                'voice_used': voice,
                'environmental_impact': impact,
                'audio_url': f'/api/audio/{audio_filename}'
            }
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/audio/<filename>')
def get_audio(filename):
    """Serve audio files"""
    return send_from_directory(app.config['AUDIO_FOLDER'], filename)

@app.route('/api/voices', methods=['GET'])
def get_available_voices():
    """Get list of available ElevenLabs voices"""
    voices = set()
    for category in ECO_MESSAGES.values():
        for message in category:
            if isinstance(message, dict) and 'voice' in message:
                voices.add(message['voice'])
    
    return jsonify({
        'status': 'success',
        'data': {
            'available_voices': list(voices)
        }
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get environmental impact statistics"""
    try:
        with open('transaction_log.json', 'r') as f:
            transactions = [json.loads(line) for line in f]
        
        total_impact = {
            'paper_saved': 0,
            'trees_saved': 0,
            'carbon_saved': 0,
            'water_saved': 0
        }
        
        for transaction in transactions:
            amount = float(transaction['transaction']['amount'])
            impact = processor.calculate_environmental_impact(amount)
            for key in total_impact:
                total_impact[key] += impact[key]
        
        return jsonify({
            'status': 'success',
            'data': {
                'total_transactions': len(transactions),
                'environmental_impact': total_impact
            }
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

def cleanup_audio_files():
    """Remove old audio files"""
    current_time = datetime.now().timestamp()
    audio_dir = app.config['AUDIO_FOLDER']
    
    for filename in os.listdir(audio_dir):
        filepath = os.path.join(audio_dir, filename)
        if current_time - os.path.getmtime(filepath) > app.config['MAX_AUDIO_AGE']:
            os.remove(filepath)

if __name__ == '__main__':
    app.run(debug=True)