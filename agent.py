from flask import Flask, render_template, request, jsonify
import cohere
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime

app = Flask(__name__)

# Initialize Cohere client - replace with your API key
co = cohere.Client('dnTP9WbkjF5EU8QRVYsOdrdbKwjzqAQk0pm4kiay')

# Store transactions in memory (in a real app, you'd use a database)
transactions = [
    {
        "date": "2024-01-15",
        "product": "Laptop",
        "category": "Electronics",
        "amount": 1200,
        "carbon_footprint": 120  # in kg CO2
    }
]

def analyze_transaction(transaction_data):
    # Create a prompt for Cohere to analyze the transaction
    prompt = f"""
    Analyze the following transaction for carbon emission impact and provide recommendations in JSON format.
    
    Transaction Details:
    - Product: {transaction_data['product']}
    - Category: {transaction_data['category']}
    - Amount: ${transaction_data['amount']}
    - Carbon Footprint: {transaction_data['carbon_footprint']} kg CO2

    Please provide an analysis and suggestions to reduce carbon emissions for similar future purchases.
    Consider:
    1. Alternative products with lower emissions
    2. Usage optimization
    3. End-of-life recycling
    4. Transportation impact
    
    Respond with valid JSON in this exact format:
    {{
        "analysis": "detailed analysis here",
        "suggestions": ["suggestion1", "suggestion2", "suggestion3"],
        "estimated_savings": numeric_value
    }}
    """
    
    try:
        response = co.generate(
            model='command',
            prompt=prompt,
            max_tokens=500,
            temperature=0.7,
            stop_sequences=["}"],
            stream=False
        )
        
        # Extract JSON from the response
        response_text = response.generations[0].text + "}"  # Add closing brace since we used stop_sequences
        return json.loads(response_text)
    except Exception as e:
        print(f"Error in analyze_transaction: {str(e)}")
        # Return fallback analysis if Cohere fails
        return {
            "analysis": f"Analysis of {transaction_data['product']}: This transaction resulted in {transaction_data['carbon_footprint']} kg of CO2 emissions.",
            "suggestions": [
                "Consider purchasing energy-efficient alternatives",
                "Look for products with eco-friendly certifications",
                "Evaluate the product's entire lifecycle impact"
            ],
            "estimated_savings": round(transaction_data['carbon_footprint'] * 0.3)  # Estimate 30% potential savings
        }

def create_emissions_chart(transactions_data):
    df = pd.DataFrame(transactions_data)
    fig = px.bar(
        df,
        x='date',
        y='carbon_footprint',
        color='category',
        title='Carbon Emissions by Transaction'
    )
    return json.loads(fig.to_json())

def create_category_breakdown(transactions_data):
    df = pd.DataFrame(transactions_data)
    category_totals = df.groupby('category')['carbon_footprint'].sum().reset_index()
    fig = px.pie(
        category_totals,
        values='carbon_footprint',
        names='category',
        title='Carbon Emissions by Category'
    )
    return json.loads(fig.to_json())

@app.route('/')
def index():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Carbon Emission Analysis</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100">
    <div class="container mx-auto px-4 py-8">
        <h1 class="text-3xl font-bold mb-8">Carbon Emission Analysis</h1>
        
        <div class="bg-white rounded-lg shadow-md p-6 mb-8">
            <h2 class="text-xl font-semibold mb-4">Add New Transaction</h2>
            <div class="grid grid-cols-1 gap-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700">Product Name</label>
                    <input type="text" id="product" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700">Category</label>
                    <input type="text" id="category" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700">Amount ($)</label>
                    <input type="number" id="amount" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700">Carbon Footprint (kg CO2)</label>
                    <input type="number" id="carbon_footprint" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500">
                </div>
                <button onclick="analyzeTransaction()" class="bg-green-500 text-white px-4 py-2 rounded-md hover:bg-green-600 transition-colors">
                    Analyze Transaction
                </button>
            </div>
        </div>

        <div id="loading" class="hidden">
            <div class="flex items-center justify-center p-4">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-green-500"></div>
            </div>
        </div>

        <div id="error-message" class="hidden bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-8"></div>

        <div id="analysis-container" class="hidden">
            <div class="bg-white rounded-lg shadow-md p-6 mb-8">
                <h2 class="text-xl font-semibold mb-4">Analysis Results</h2>
                <div id="analysis-text" class="prose"></div>
                <div id="suggestions-list" class="mt-4 space-y-2"></div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div class="bg-white rounded-lg shadow-md p-6">
                    <div id="emissions-chart" class="h-96"></div>
                </div>
                <div class="bg-white rounded-lg shadow-md p-6">
                    <div id="category-chart" class="h-96"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function showLoading() {
            document.getElementById('loading').classList.remove('hidden');
            document.getElementById('error-message').classList.add('hidden');
        }

        function hideLoading() {
            document.getElementById('loading').classList.add('hidden');
        }

        function showError(message) {
            const errorDiv = document.getElementById('error-message');
            errorDiv.textContent = message;
            errorDiv.classList.remove('hidden');
        }

        function validateInputs() {
            const product = document.getElementById('product').value;
            const category = document.getElementById('category').value;
            const amount = document.getElementById('amount').value;
            const carbon_footprint = document.getElementById('carbon_footprint').value;

            if (!product || !category || !amount || !carbon_footprint) {
                showError('Please fill in all fields');
                return false;
            }
            return true;
        }

        async function analyzeTransaction() {
            if (!validateInputs()) return;

            const transaction = {
                product: document.getElementById('product').value,
                category: document.getElementById('category').value,
                amount: parseFloat(document.getElementById('amount').value),
                carbon_footprint: parseFloat(document.getElementById('carbon_footprint').value)
            };

            showLoading();

            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(transaction)
                });

                const data = await response.json();

                if (!data.success && data.error) {
                    throw new Error(data.error);
                }

                // Show analysis container
                document.getElementById('analysis-container').classList.remove('hidden');

                // Update analysis text
                document.getElementById('analysis-text').innerHTML = `
                    <p class="mb-4">${data.analysis.analysis}</p>
                    <p class="text-green-600 font-semibold">Potential CO2 Savings: ${data.analysis.estimated_savings} kg</p>
                `;

                // Update suggestions
                const suggestionsList = document.getElementById('suggestions-list');
                suggestionsList.innerHTML = '<h3 class="font-semibold mb-2">Recommendations for Reduction:</h3>';
                data.analysis.suggestions.forEach(suggestion => {
                    suggestionsList.innerHTML += `
                        <div class="bg-green-50 border-l-4 border-green-500 p-4">
                            ${suggestion}
                        </div>
                    `;
                });

                // Update charts
                Plotly.newPlot('emissions-chart', data.emissions_chart.data, data.emissions_chart.layout);
                Plotly.newPlot('category-chart', data.category_chart.data, data.category_chart.layout);

                // Clear form
                document.getElementById('product').value = '';
                document.getElementById('category').value = '';
                document.getElementById('amount').value = '';
                document.getElementById('carbon_footprint').value = '';

            } catch (error) {
                showError('Error analyzing transaction: ' + error.message);
            } finally {
                hideLoading();
            }
        }
    </script>
</body>
</html>
"""

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        transaction = request.json
        
        # Add timestamp if not provided
        if 'date' not in transaction:
            transaction['date'] = datetime.now().strftime('%Y-%m-%d')
        
        # Add to transactions list
        transactions.append(transaction)
        
        # Perform analysis using Cohere
        analysis_result = analyze_transaction(transaction)
        
        # Create visualizations
        emissions_chart = create_emissions_chart(transactions)
        category_chart = create_category_breakdown(transactions)
        
        return jsonify({
            'success': True,
            'analysis': analysis_result,
            'emissions_chart': emissions_chart,
            'category_chart': category_chart
        })
    except Exception as e:
        print(f"Error in /analyze endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)