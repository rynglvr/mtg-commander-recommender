# 🧙‍♂️ MTG Commander Deck Recommender

An AI-powered Magic: The Gathering Commander deck recommendation system that suggests cards with high synergy while respecting color identity rules.

## ✨ Features

- **Content-Based Filtering**: Uses machine learning to find cards with similar mechanics and text
- **Color Identity Compliance**: Only recommends cards legal in your commander's color identity  
- **Web Interface**: Clean, user-friendly web app for easy card discovery
- **Budget Conscious**: Focuses on cards under $10
- **Keyword-Based Similarity**: Matches on important MTG mechanics like proliferate, defender, artifacts, etc.

## 🚀 How It Works

1. **Data Collection**: Gathers 4,000+ Commander-legal cards under $10 from Scryfall API
2. **Feature Extraction**: Converts card text into numerical features based on MTG keywords
3. **Similarity Calculation**: Uses cosine similarity to find mechanically similar cards
4. **Color Filtering**: Ensures all recommendations are legal in the commander's color identity
5. **Web Interface**: Presents results in an intuitive web application

## 🛠️ Technology Stack

- **Python 3.11**: Core programming language
- **scikit-learn**: Machine learning algorithms
- **TensorFlow**: ML framework (with Apple Silicon optimization)
- **Flask**: Web framework
- **Pandas**: Data manipulation
- **Scryfall API**: MTG card data source

## 🏃‍♂️ Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mtg-commander-recommender.git
   cd mtg-commander-recommender

2. **Set up Python environment**
   python3.11 -m venv mtg-env
   source mtg-env/bin/activate  # On Windows: mtg-env\Scripts\activate
   pip install -r requirements.txt

3. **Run data collection**
   jupyter notebook
   Run 01_data_exploration.ipynb to collect fresh data

4. **Start app**
   python app.py

5. **Run app**
   Open your browser to http://localhost:5000

## 🧠 ML Approach
This project uses content-based filtering to recommend cards by analyzing MTG-specific keywords and mechanics rather than generic text similarity.

## 🙏 Acknowledgments

Scryfall API for MTG data
The MTG community for deck building insights

Magic: The Gathering is © Wizards of the Coast

## 🆕 Recent Enhancements

### v2.0 - Comprehensive Multi-Word Keyword System
- **Expanded Keyword Coverage**: From 28 to 100+ keywords including multi-word phrases
- **Better Phrase Matching**: Now recognizes "enters the battlefield", "combat damage", "+1/+1 counter", etc.
- **Improved Recommendations**: Dramatically better suggestions for complex commanders
- **Zero Similarity Fix**: Resolved issues where commanders got no meaningful recommendations
- **Enhanced Tribal Support**: Better recognition of creature types and tribal synergies

### Key Improvements:
- **Multi-word phrases**: "first strike", "artifact creature", "whenever you cast"
- **Triggered abilities**: "when enters", "at the beginning of", "whenever attacks"  
- **Combat mechanics**: "combat damage", "attacking creature", "blocking creature"
- **Counter synergies**: "+1/+1 counter", "proliferate", "counter on it"
- **Tribal keywords**: All major creature types (Human, Elf, Goblin, etc.)

## 🎯 Examples of Improved Recommendations

**Before**: Isshin returned cards with 0% similarity  
**After**: Isshin now finds relevant combat and triggered ability synergies

**Before**: Limited to single-word matches like "flying" or "artifact"  
**After**: Recognizes complex phrases like "whenever this creature attacks"

