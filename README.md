# AI Fashion Recommendation System

This project is a fashion recommendation system built in Python that suggests clothing items based on user preferences such as color, occasion, style tags, and budget.
It also includes a simple feedback system (like/dislike) so recommendations improve over time.

The project has a web interface created with Streamlit, allowing users to interact with the system in a browser.

## What This Project Does

-Lets users enter their style preferences (colors, occasion, tags, budget)
-Ranks clothing items using a similarity-based scoring system
-Displays the top recommendations in a web app
-Allows users to like or dislike items
-Saves feedback and uses it to improve future recommendations

This project was built to practice combining AI concepts, data processing, and web application development into one complete system.

## How It Works (Simple Explanation)

1. The user enters their preferences.
2. Each clothing item is compared to those preferences using a similarity score.
3. Items are ranked based on:
   -how well they match the user’s style
   -whether they fit the user’s budget
   -feedback from previous likes and dislikes
4. The system shows the best matches.
5. When the user clicks like or dislike, the system updates its internal weights so future recommendations are more personalized.

## Tech Stack
- Python
- Pandas
- NumPy
- Streamlit
- JSON (to store user feedback)

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
