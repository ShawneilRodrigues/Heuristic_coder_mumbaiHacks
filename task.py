from flask import Flask, request, jsonify
import cohere
import pandas as pd
import json
import plotly.express as px
from datetime import datetime

app = Flask(__name__)

# Initialize Cohere client
co = cohere.Client('dnTP9WbkjF5EU8QRVYsOdrdbKwjzqAQk0pm4kiay')

# Store transactions in memory
transactions = []

def predict_carbon_footprint(product, category, amount):
    """
    Predict carbon footprint using Cohere LLM based on product details
    """
    prompt = f"""
    Predict the carbon footprint (in kg CO2) for the following purchase based on typical lifecycle emissions.
    Only respond with a number representing kg CO2e.
    
    Product: {product}
    Category: {category}
    Price: ${amount}

    Consider:
    1. Manufacturing emissions
    2. Transportation footprint
    3. Average usage energy consumption
    4. End-of-life disposal impact
    5. Industry standards and averages
    
    Response example: 120.5
    """
    
    try:
        response = co.generate(
            model='command',
            prompt=prompt,
            max_tokens=10,
            temperature=0.1,
            stream=False
        )
        predicted_footprint = float(response.generations[0].text.strip())
        return max(0, round(predicted_footprint, 2))
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        # Fallback estimation based on amount
        return round(amount * 0.1, 2)

def get_recommendations(product, category, amount, footprint):
    """
    Get eco-friendly recommendations using Cohere
    """
    prompt = f"""
    Provide eco-friendly recommendations for the following purchase:
    
    Product: {product}
    Category: {category}
    Price: ${amount}
    Estimated Carbon Footprint: {footprint} kg CO2

    Provide recommendations in JSON format:
    {{
        "impact_level": "low/medium/high",
        "analysis": "brief analysis here",
        "recommendations": ["specific recommendation 1", "specific recommendation 2", "specific recommendation 3"],
        "potential_savings": "estimated CO2 savings in kg"
    }}
    """
    
    try:
        response = co.generate(
            model='command',
            prompt=prompt,
            max_tokens=500,
            temperature=0.7,
            stop_sequences=["}"]
        )
        return json.loads(response.generations[0].text + "}")
    except Exception as e:
        print(f"Recommendation error: {str(e)}")
        return {
            "impact_level": "medium",
            "analysis": f"This {product} has an estimated carbon footprint of {footprint} kg CO2",
            "recommendations": [
                f"Consider energy-efficient {category} alternatives",
                "Look for products with environmental certifications",
                "Research manufacturers with sustainable practices"
            ],
            "potential_savings": round(footprint * 0.3, 2)
        }

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['product', 'category', 'amount']
        if not all(field in data for field in required_fields):
            return jsonify({
                'error': 'Please provide product, category, and amount'
            }), 400
        
        # Predict carbon footprint
        footprint = predict_carbon_footprint(
            data['product'], 
            data['category'], 
            data['amount']
        )
        
        # Get recommendations
        recommendations = get_recommendations(
            data['product'],
            data['category'],
            data['amount'],
            footprint
        )
        
        # Create transaction record
        transaction = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'product': data['product'],
            'category': data['category'],
            'amount': data['amount'],
            'carbon_footprint': footprint
        }
        
        # Store transaction
        transactions.append(transaction)
        
        # Create visualizations if we have multiple transactions
        charts = {}
        if len(transactions) > 1:
            df = pd.DataFrame(transactions)
            
            # Emissions over time
            time_chart = px.bar(
                df,
                x='date',
                y='carbon_footprint',
                color='category',
                title='Carbon Emissions by Transaction'
            )
            
            # Category breakdown
            category_totals = df.groupby('category')['carbon_footprint'].sum().reset_index()
            category_chart = px.pie(
                category_totals,
                values='carbon_footprint',
                names='category',
                title='Emissions by Category'
            )
            
            charts = {
                'time_series': time_chart.to_json(),
                'category_breakdown': category_chart.to_json()
            }
        
        return jsonify({
            'transaction': transaction,
            'predictions': {
                'carbon_footprint': footprint,
                'impact_assessment': recommendations['impact_level'],
                'analysis': recommendations['analysis'],
                'recommendations': recommendations['recommendations'],
                'potential_savings': recommendations['potential_savings']
            },
            'visualizations': charts
        })

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/transactions', methods=['GET'])
def get_transactions():
    return jsonify({
        'transactions': transactions,
        'total_footprint': sum(t['carbon_footprint'] for t in transactions),
        'average_footprint': round(sum(t['carbon_footprint'] for t in transactions) / len(transactions), 2) if transactions else 0
    })

if __name__ == '__main__':
    app.run(debug=True)