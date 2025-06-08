
from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import ast

app = Flask(__name__)

# Define color functions directly in this file
def get_color_identity(colors_string):
    """Convert color string to set for easier comparison"""
    if pd.isna(colors_string) or colors_string == '[]':
        return set()
    try:
        colors_list = ast.literal_eval(colors_string)
        return set(colors_list) if colors_list else set()
    except:
        return set()

def is_legal_in_deck(card_colors_string, commander_colors_string):
    """Check if card is legal in commander's color identity"""
    card_identity = get_color_identity(card_colors_string)
    commander_identity = get_color_identity(commander_colors_string)
    return card_identity.issubset(commander_identity)

# Load our saved model (without the functions)
print("Loading ML model...")
with open('data/mtg_model.pkl', 'rb') as f:
    model_data = pickle.load(f)

df_clean = model_data['df_clean']
keyword_matrix = model_data['keyword_matrix']
keywords = model_data['keywords']

print(f"Model loaded! {len(df_clean)} cards available")

def find_recommendations(commander_name, num_recommendations=10):
    """Main recommendation function for web app"""
    # Find commander
    card_matches = df_clean[df_clean['name'].str.contains(commander_name, case=False, na=False)]

    if len(card_matches) == 0:
        return {"error": f"Commander '{commander_name}' not found"}

    commander_row = card_matches.iloc[0]
    commander_idx = card_matches.index[0]
    commander_colors = commander_row['colors']
    commander_vector = keyword_matrix[commander_idx].reshape(1, -1)

    # Calculate similarities
    similarities = cosine_similarity(commander_vector, keyword_matrix).flatten()
    all_indices = similarities.argsort()[::-1]

    # Filter for legal cards
    results = []
    for idx in all_indices:
        if idx == commander_idx:
            continue

        card_row = df_clean.iloc[idx]
        if is_legal_in_deck(card_row['colors'], commander_colors):
            results.append({
                'name': card_row['name'],
                'similarity': float(similarities[idx]),
                'type': card_row['type_line'],
                'colors': list(get_color_identity(card_row['colors'])),
                'text': card_row['oracle_text'][:200] + "..." if len(card_row['oracle_text']) > 200 else card_row['oracle_text'],
                'price': card_row.get('usd', 'N/A')
            })

            if len(results) >= num_recommendations:
                break

    return {
        "commander": {
            "name": commander_row['name'],
            "colors": list(get_color_identity(commander_colors)),
            "type": commander_row['type_line']
        },
        "recommendations": results
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    commander = data.get('commander', '')
    num_recs = data.get('num_recommendations', 10)

    result = find_recommendations(commander, num_recs)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
