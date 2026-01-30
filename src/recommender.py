import argparse
import math
from dataclasses import dataclass
from typing import List, Dict, Tuple

import numpy as np
import pandas as pd
import json
from pathlib import Path

FEEDBACK_PATH = Path("data/feedback.json")

def load_feedback() -> dict:
    if FEEDBACK_PATH.exists():
        try:
            return json.loads(FEEDBACK_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}

def save_feedback(feedback: dict) -> None:
    FEEDBACK_PATH.parent.mkdir(parents=True, exist_ok=True)
    FEEDBACK_PATH.write_text(json.dumps(feedback, indent=2), encoding="utf-8")

def update_tag_weights(feedback: dict, liked_tags: list[str], disliked_tags: list[str]) -> None:
    learned = feedback.get("tag_weights", {})
    lr = 0.2

    for t in liked_tags:
        t = t.strip().lower()
        if t:
            learned[t] = float(learned.get(t, 0.0)) + lr

    for t in disliked_tags:
        t = t.strip().lower()
        if t:
            learned[t] = float(learned.get(t, 0.0)) - lr

    feedback["tag_weights"] = learned


@dataclass
class UserPrefs:
    colors: List[str]
    occasion: str
    tags: List[str]
    budget: float
    top_k: int


def normalize_list(values: str) -> List[str]:
    if not values:
        return []
    return [v.strip().lower() for v in values.split(",") if v.strip()]


def build_tag_vocab(items_tags: pd.Series) -> Dict[str, int]:
    vocab = {}
    for tags in items_tags:
        for t in normalize_list(tags):
            if t not in vocab:
                vocab[t] = len(vocab)
    return vocab


def tags_to_vec(tags: str, vocab: Dict[str, int]) -> np.ndarray:
    vec = np.zeros(len(vocab), dtype=float)
    for t in normalize_list(tags):
        if t in vocab:
            vec[vocab[t]] = 1.0
    return vec


def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


def score_item(row: pd.Series, user: UserPrefs, user_vec: np.ndarray, vocab: Dict[str, int]) -> float:
    """
    Hybrid score:
      - tag cosine similarity (main signal)
      - color match boost
      - occasion match boost
      - budget penalty if over budget
    """
    item_vec = tags_to_vec(row["style_tags"], vocab)
    tag_score = cosine_sim(user_vec, item_vec)  # 0..1

    # boosts
    color = str(row["color"]).strip().lower()
    occasion = str(row["occasion"]).strip().lower()
    price = float(row["price"])

    color_boost = 0.15 if color in user.colors else 0.0
    occasion_boost = 0.15 if occasion == user.occasion else 0.0

    # budget handling: soft penalty if slightly above, stronger if far above
    if price <= user.budget:
        budget_factor = 1.0
    else:
        over = price - user.budget
        budget_factor = math.exp(-over / max(user.budget, 1.0))  # decays smoothly

    score = (0.7 * tag_score + color_boost + occasion_boost) * budget_factor
    return float(score)


def recommend(items: pd.DataFrame, user: UserPrefs, feedback: dict | None = None) -> pd.DataFrame:
    if feedback is None:
        feedback = {}
    # vocab from dataset
    vocab = build_tag_vocab(items["style_tags"])
    user_vec = tags_to_vec(",".join(user.tags), vocab)

    scores = []
    for _, row in items.iterrows():
        s = score_item(row, user, user_vec, vocab)
        scores.append(s)

    out = items.copy()
    out["score"] = scores
    out = out.sort_values("score", ascending=False).head(user.top_k)
    return out[["item_id", "name", "category", "color", "occasion", "style_tags", "price", "score"]]


def prompt_user_prefs() -> UserPrefs:
    print("\nAI Fashion Recommender — quick preferences\n")

    colors = normalize_list(input("Preferred colors (comma-separated, e.g. black, white): ").strip())
    if not colors:
        colors = ["black", "white"]

    occasion = input("Occasion (casual / formal / work / date / night-out): ").strip().lower()
    if occasion not in {"casual", "formal", "work", "date", "night-out", "smart-casual"}:
        occasion = "casual"

    tags = normalize_list(input("Style tags (comma-separated, e.g. minimal, streetwear): ").strip())
    if not tags:
        tags = ["minimal", "comfortable"]

    budget_raw = input("Max budget in USD (e.g. 100): ").strip()
    try:
        budget = float(budget_raw)
    except ValueError:
        budget = 100.0

    top_k_raw = input("How many recommendations? (e.g. 5): ").strip()
    try:
        top_k = int(top_k_raw)
    except ValueError:
        top_k = 5

    return UserPrefs(colors=colors, occasion=occasion, tags=tags, budget=budget, top_k=top_k)


def main():
    parser = argparse.ArgumentParser(description="AI Fashion Recommendation System (simple hybrid scorer).")
    parser.add_argument("--data", default="data/items.csv", help="Path to items CSV.")
    parser.add_argument("--interactive", action="store_true", help="Prompt for user preferences.")
    parser.add_argument("--colors", default="", help="Comma-separated preferred colors.")
    parser.add_argument("--occasion", default="casual", help="Occasion.")
    parser.add_argument("--tags", default="", help="Comma-separated style tags.")
    parser.add_argument("--budget", type=float, default=100.0, help="Max budget in USD.")
    parser.add_argument("--top_k", type=int, default=5, help="Number of recommendations.")
    args = parser.parse_args()

    items = pd.read_csv(args.data)

    if args.interactive:
        user = prompt_user_prefs()
    else:
        user = UserPrefs(
            colors=normalize_list(args.colors) or ["black", "white"],
            occasion=args.occasion.strip().lower(),
            tags=normalize_list(args.tags) or ["minimal", "comfortable"],
            budget=args.budget,
            top_k=args.top_k,
        )

    recs = recommend(items, user)

    print("\nTop recommendations:\n")
    for _, r in recs.iterrows():
        print(f"- {r['name']} (${r['price']:.0f}) | {r['category']} | {r['color']} | {r['occasion']} | score={r['score']:.3f}")

    print("\nTip: try different tags/colors to see how rankings change!\n")


if __name__ == "__main__":
    main()
