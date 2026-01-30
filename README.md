# AI Fashion Recommendation System

A Python-based fashion recommendation system that suggests outfits based on user preferences such as:
- preferred colors
- occasion
- style tags
- budget

The system ranks items using similarity scoring and produces personalized recommendations.

## Features
- Interactive web interface using Streamlit
- Personalized recommendations based on user preferences
- Feedback system (like/dislike) that improves results over time
- Budget-aware and similarity-based ranking

## Tech Stack
- Python
- Pandas
- NumPy

## Example Output
- White Sneakers ($60) | shoes | white | casual  
- Graphic Tee ($30) | top | black | casual  
- Oversized Hoodie ($55) | top | gray | casual  

## Future Improvements
- Deploy the app online (Streamlit Cloud)
- Add more clothing items and categories
- Integrate machine learning models for smarter recommendations

## Run the Web App
```bash
pip install -r requirements.txt
streamlit run app.py
