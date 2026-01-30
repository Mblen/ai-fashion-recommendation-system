import json
from pathlib import Path

import pandas as pd
import streamlit as st

from src.recommender import UserPrefs, recommend, normalize_list, load_feedback, save_feedback, update_tag_weights

st.set_page_config(page_title="AI Fashion Recommender", page_icon="👗")

DATA_PATH = Path("data/items.csv")

st.title("👗 AI Fashion Recommendation System")
st.caption("Personalized recommendations using preferences + learned feedback.")

items = pd.read_csv(DATA_PATH)
feedback = load_feedback()

st.sidebar.header("Your Preferences")
colors = st.sidebar.text_input("Preferred colors (comma-separated)", value="black, white")
occasion = st.sidebar.selectbox("Occasion", ["casual", "formal", "work", "date", "night-out", "smart-casual"], index=0)
tags = st.sidebar.text_input("Style tags (comma-separated)", value="minimal, streetwear")
budget = st.sidebar.number_input("Max budget ($)", min_value=0, value=100, step=5)
top_k = st.sidebar.slider("How many recommendations?", min_value=1, max_value=10, value=5)

user = UserPrefs(
    colors=normalize_list(colors),
    occasion=occasion,
    tags=normalize_list(tags),
    budget=float(budget),
    top_k=int(top_k),
)

recs = recommend(items, user, feedback)

st.subheader("Top Recommendations")
for _, r in recs.iterrows():
    st.write(f"**{int(r['item_id'])}. {r['name']}** — ${float(r['price']):.0f}  \n"
             f"{r['category']} | {r['color']} | {r['occasion']}  \n"
             f"Tags: {r['style_tags']}  \n"
             f"Score: {float(r['score']):.3f}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"👍 Like {int(r['item_id'])}", key=f"like_{int(r['item_id'])}"):
            liked_tags = normalize_list(r["style_tags"])
            update_tag_weights(feedback, liked_tags, [])
            save_feedback(feedback)
            st.success("Saved like! Next refresh will adapt.")

    with col2:
        if st.button(f"👎 Dislike {int(r['item_id'])}", key=f"dislike_{int(r['item_id'])}"):
            disliked_tags = normalize_list(r["style_tags"])
            update_tag_weights(feedback, [], disliked_tags)
            save_feedback(feedback)
            st.warning("Saved dislike! Next refresh will adapt.")

st.divider()
st.subheader("Learned Preferences")
st.write(feedback.get("tag_weights", {}))
st.caption("Your feedback helps tailor future recommendations!")