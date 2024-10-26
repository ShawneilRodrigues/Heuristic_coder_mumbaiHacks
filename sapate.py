from flask import Flask, jsonify, request, render_template_string
import cohere
import os
import random
from datetime import datetime
import uuid
import json

app = Flask(__name__)

# Configuration
app.config['COHERE_API_KEY'] = 'zdOo8nXVDqdfHC1BI3CMMb8w9H8X9KER7EA3YJn6'
app.config['ELEVEN_LABS_API_KEY'] = 'sk_1f0bf4cd533a480a16780becfab8c5b4da9fe3731a458c15'

# HTML template as a string
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Eco-friendly Digital Banking</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.7.0/chart.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f0f8f1;
            color: #2c3e50;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }

        h1 {
            color: #2ecc71;
            text-align: center;
            margin-bottom: 30px;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 5px;
            color: #34495e;
        }

        input[type="number"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #bdc3c7;
            border-radius: 5px;
            font-size: 16px;
        }

        button {
            background-color: #2ecc71;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
            transition: background-color 0.3s;
        }

        button:hover {
            background-color: #27ae60;
        }

        .result {
            margin-top: 20px;
            padding: 15px;
            border-radius: 5px;
            background-color: #e8f6e9;
            display: none;
        }

        .stats {
            margin-top: 30px;
            padding: 20px;
            background-color: #f7f9fc;
            border-radius: 5px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 15px;
        }

        .stat-card {
            background-color: white;
            padding: 15px;
            border-radius: 5px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }

        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #2ecc71;
        }

        .loading {
            display: none;
            text-align: center;
            margin: 20px 0;
        }

        .error {
            background-color: #fde8e8;
            color: #c53030;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌿 Eco-friendly Digital Banking</h1>
        
        <div class="form-group">
            <label for="amount">Transaction Amount ($)</label>
            <input type="number" id="amount" min="0" step="0.01" required>
        </div>

        <button onclick="processTransaction()">Process Transaction</button>

        <div id="loading" class="loading">
            Processing transaction...
        </div>

        <div id="error" class="error"></div>

        <div id="result" class="result">
            <h3>Transaction Processed!</h3>
            <p id="eco-message"></p>
            <p><strong>Voice Used:</strong> <span id="voice-used"></span></p>
        </div>

        <div class="stats">
            <h3>Environmental Impact Statistics</h3>
            <div class="stats-grid">
                <div class="stat-card">
                    <div>Total Transactions</div>
                    <div id="total-transactions" class="stat-value">0</div>
                </div>
                <div class="stat-card">
                    <div>Paper Saved</div>
                    <div id="paper-saved" class="stat-value">0g</div>
                </div>
                <div class="stat-card">
                    <div>Trees Saved</div>
                    <div id="trees-saved" class="stat-value">0</div>
                </div>
                <div class="stat-card">
                    <div>Carbon Reduced</div>
                    <div id="carbon-saved" class="stat-value">0g</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Load initial statistics
        loadStats();

        async function processTransaction() {
            const amount = document.getElementById('amount').value;
            const loading = document.getElementById('loading');
            const error = document.getElementById('error');
            const result = document.getElementById('result');

            if (!amount || amount <= 0) {
                showError('Please enter a valid amount');
                return;
            }

            loading.style.display = 'block';
            error.style.display = 'none';
            result.style.display = 'none';

            try {
                const response = await fetch('/api/transaction', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ amount: parseFloat(amount) })
                });

                const data = await response.json();

                if (data.status === 'success') {
                    document.getElementById('eco-message').textContent = data.data.eco_message;
                    document.getElementById('voice-used').textContent = data.data.voice_used;
                    result.style.display = 'block';
                    
                    // Reload stats after successful transaction
                    loadStats();
                } else {
                    showError(data.message);
                }
            } catch (err) {
                showError('Failed to process transaction. Please try again.');
            } finally {
                loading.style.display = 'none';
            }
        }

        async function loadStats() {
            try {
                const response = await fetch('/api/stats');
                const data = await response.json();

                if (data.status === 'success') {
                    document.getElementById('total-transactions').textContent = data.data.total_transactions;
                    document.getElementById('paper-saved').textContent = 
                        `${data.data.environmental_impact.paper_saved.toFixed(1)}g`;
                    document.getElementById('trees-saved').textContent = 
                        data.data.environmental_impact.trees_saved.toFixed(3);
                    document.getElementById('carbon-saved').textContent = 
                        `${data.data.environmental_impact.carbon_saved.toFixed(1)}g`;
                }
            } catch (err) {
                console.error('Failed to load statistics:', err);
            }
        }

        function showError(message) {
            const error = document.getElementById('error');
            error.textContent = message;
            error.style.display = 'block';
        }
    </script>
</body>
</html>
'''

# Initialize API clients
co = cohere.Client(app.config['COHERE_API_KEY'])

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

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

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
        
        # Log transaction
        processor.log_transaction(data, eco_message)
        
        return jsonify({
            'status': 'success',
            'data': {
                'transaction_id': str(uuid.uuid4()),
                'eco_message': eco_message,
                'voice_used': voice,
                'environmental_impact': impact
            }
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

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

if __name__ == '__main__':
    app.run(debug=True)