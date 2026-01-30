# 👗 AI Fashion Recommendation System

An interactive fashion recommendation web application that suggests outfits based on user preferences using similarity-based ranking and a feedback learning loop.

This project explores how AI can be applied to fashion technology by adapting recommendations over time based on user likes and dislikes.

---

## 🚀 Features
- Content-based recommendation using cosine similarity
- User preference input (style, color, category)
- Like / Dislike feedback system to adapt ranking
- Persistent feedback storage (JSON file)
- Interactive web interface built with Streamlit

---

## 🧠 How It Works
1. The user selects fashion preferences (style, color, category).
2. The system calculates similarity scores between user input and dataset items.
3. Top recommendations are displayed.
4. User feedback (like/dislike) is saved and used to re-rank future recommendations.

---

## 📊 Evaluation
The system was tested using 30 simulated user preference queries.  
Top-3 recommendations contained at least one relevant item in **83% of cases**.

---

## 🛠 Tech Stack
- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- JSON storage

---

## ▶️ Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
