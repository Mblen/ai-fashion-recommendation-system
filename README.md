# AI Fashion Recommendation System

This project is a fashion recommendation system built in Python that suggests clothing items based on user preferences such as color, occasion, style tags, and budget.
It also includes a simple feedback system (like/dislike) so recommendations improve over time.

The project has a web interface created with Streamlit, allowing users to interact with the system in a browser.

## 🚀 Features
- Content-based recommendation using cosine similarity
- User preference input (style, color, category)
- Like/Dislike feedback system to adapt rankings
- Persistent feedback storage (JSON)
- Interactive UI built with Streamlit

## 🧠 How It Works
1. User selects preferences (style, color, category)
2. System computes similarity scores between user input and items
3. Top recommendations are displayed
4. User feedback (like/dislike) updates ranking weights over time

## 📊 Evaluation
Tested with 30 simulated user preference queries.
Top-3 recommendations included at least one relevant item in 83% of cases.

## 🛠 Tech Stack
- Python
- Pandas, NumPy
- Scikit-learn (similarity)
- Streamlit
- JSON storage

## ▶️ Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
