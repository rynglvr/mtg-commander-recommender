
from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import ast
import json

app = Flask(__name__)

# Color identity functions
def get_color_identity(colors_string):
    if pd.isna(colors_string) or colors_string == '[]':
        return set()
    try:
        colors_list = ast.literal_eval(colors_string)
        return set(colors_list) if colors_list else set()
    except:
        return set()

def is_legal_in_deck(card_colors_string, commander_colors_string):
    card_identity = get_color_identity(card_colors_string)
    commander_identity = get_color_identity(commander_colors_string)
    return card_identity.issubset(commander_identity)

def get_card_image_url(row, size='normal'):
    """Extract card image URL from the image_uris field"""
    try:
        if 'image_uris' not in row or pd.isna(row['image_uris']):
            return None

        image_uris = row['image_uris']

        if isinstance(image_uris, str):
            try:
                image_dict = ast.literal_eval(image_uris)
            except:
                try:
                    image_dict = json.loads(image_uris)
                except:
                    return None
        elif isinstance(image_uris, dict):
            image_dict = image_uris
        else:
            return None

        size_priority = [size, 'normal', 'small', 'large']
        for sz in size_priority:
            if sz in image_dict:
                return image_dict[sz]

        return list(image_dict.values())[0] if image_dict else None

    except Exception as e:
        print(f"Error getting image for {row.get('name', 'unknown')}: {e}")
        return None

def get_card_price(row):
    """Extract USD price from the prices field"""
    try:
        if 'prices' not in row or pd.isna(row['prices']):
            return None

        prices_str = row['prices']

        if isinstance(prices_str, str):
            try:
                prices_dict = ast.literal_eval(prices_str)

                usd_price = prices_dict.get('usd')

                if usd_price is not None and usd_price != 'None' and usd_price != '':
                    try:
                        price_float = float(usd_price)
                        return f"{price_float:.2f}"
                    except (ValueError, TypeError):
                        return str(usd_price)

                return None

            except (ValueError, SyntaxError) as e:
                return None

        return None

    except Exception as e:
        return None

# Load enhanced model
print("Loading enhanced ML model...")
try:
    with open('data/mtg_model_enhanced.pkl', 'rb') as f:
        model_data = pickle.load(f)

    df_clean = model_data['df_clean']
    keyword_matrix = model_data['keyword_matrix']
    keywords = model_data['keywords']

    print(f"Enhanced model loaded!")
    print(f"  - {len(df_clean)} cards")
    print(f"  - {len(keywords)} keywords")

except FileNotFoundError:
    print("Enhanced model not found, using basic model...")
    with open('data/mtg_model.pkl', 'rb') as f:
        model_data = pickle.load(f)
    df_clean = model_data['df_clean']
    keyword_matrix = model_data['keyword_matrix']
    keywords = model_data['keywords']


def clean_for_json(obj):
    """Clean NaN values from objects before JSON serialization"""
    import math

    if isinstance(obj, dict):
        return {k: clean_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_for_json(item) for item in obj]
    elif isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        return None
    else:
        return obj


def clean_for_json(obj):
    """Clean NaN values from objects before JSON serialization"""
    import math

    if isinstance(obj, dict):
        return {k: clean_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_for_json(item) for item in obj]
    elif isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        return None
    else:
        return obj


def clean_for_json(obj):
    """Clean NaN values from objects before JSON serialization"""
    import math

    if isinstance(obj, dict):
        return {k: clean_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_for_json(item) for item in obj]
    elif isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        return None
    else:
        return obj


def clean_for_json(obj):
    """Clean NaN values from objects before JSON serialization"""
    import math

    if isinstance(obj, dict):
        return {k: clean_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_for_json(item) for item in obj]
    elif isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        return None
    else:
        return obj


def clean_for_json(obj):
    """Clean NaN values from objects before JSON serialization"""
    import math

    if isinstance(obj, dict):
        return {k: clean_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_for_json(item) for item in obj]
    elif isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        return None
    else:
        return obj

def find_recommendations(commander_name, num_recommendations=300):
    """Enhanced recommendation function with prices"""
    card_matches = df_clean[df_clean['name'].str.contains(commander_name, case=False, na=False)]

    if len(card_matches) == 0:
        return {"error": f"Commander '{commander_name}' not found"}

    commander_row = card_matches.iloc[0]
    commander_idx = card_matches.index[0]
    commander_colors = commander_row['colors']
    commander_vector = keyword_matrix[commander_idx].reshape(1, -1)

    similarities = cosine_similarity(commander_vector, keyword_matrix).flatten()
    all_indices = similarities.argsort()[::-1]

    results = []
    for idx in all_indices:
        if idx == commander_idx:
            continue

        card_row = df_clean.iloc[idx]
        similarity = similarities[idx]

        if similarity > 0 and is_legal_in_deck(card_row['colors'], commander_colors):
            # Get price for this card
            card_price = get_card_price(card_row)

            card_result = {
                'name': card_row['name'],
                'similarity': float(similarity),
                'type': card_row['type_line'],
                'colors': list(get_color_identity(card_row['colors'])),
                'text': card_row['oracle_text'][:200] + "..." if len(card_row['oracle_text']) > 200 else card_row['oracle_text'],
                'mana_cost': card_row.get('mana_cost', '') if pd.notna(card_row.get('mana_cost')) else '',
                'rarity': card_row.get('rarity', 'unknown'),
                'image_url': get_card_image_url(card_row, 'normal'),
                'scryfall_url': card_row.get('scryfall_uri', ''),
                'price': card_price
            }

            # Clean any NaN values
            card_result = clean_for_json(card_result)

            results.append(card_result)

            if len(results) >= num_recommendations:
                break

    response_data = {
        "commander": {
            "name": commander_row['name'],
            "colors": list(get_color_identity(commander_colors)),
            "type": commander_row['type_line'],
            "text": commander_row['oracle_text'],
            "image_url": get_card_image_url(commander_row, 'normal'),
            "scryfall_url": commander_row.get('scryfall_uri', ''),
            "price": get_card_price(commander_row)
        },
        "recommendations": results,
        "model_info": {
            "keywords_used": len(keywords),
            "version": "Enhanced Multi-Word Keywords with Images and Prices"
        }
    }

    # Clean the entire response of NaN values
    return clean_for_json(response_data)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        commander = data.get('commander', '')
        num_recs = data.get('num_recommendations', 300)

        print(f"DEBUG: Received request for {commander} with {num_recs} recommendations")

        result = find_recommendations(commander, num_recs)

        print(f"DEBUG: Successfully generated {len(result.get('recommendations', []))} recommendations")

        return jsonify(result)

    except Exception as e:
        print(f"ERROR in recommend route: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Server error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
