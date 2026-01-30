# AI Fashion Recommendation System (Python)

A simple, explainable fashion recommender that ranks clothing items based on:
- user preferences (colors, occasion, style tags)
- similarity scoring (cosine similarity on tags)
- budget-aware scoring

## Features
- Interactive CLI input (preferences)
- Hybrid scoring: tag similarity + boosts (color/occasion) + budget penalty
- Easy to extend with real user feedback or embeddings later

## Setup
```bash
pip install -r requirements.txt
