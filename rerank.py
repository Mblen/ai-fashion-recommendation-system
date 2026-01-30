from typing import List
import pandas as pd
from feedback import load_feedback

def rerank_with_feedback(
    recs: pd.DataFrame,
    catalog: pd.DataFrame,
    id_col: str = "item_id",
    tags_col: str = "tags",
    base_score_col: str = "score",
    like_boost: float = 0.15,
    dislike_penalty: float = 0.20,
) -> pd.DataFrame:
    """
    Reranks recommendations using persistent likes/dislikes.

    recs: dataframe of recommended items (must include id_col and base_score_col).
    catalog: full dataset with item_id and tags/features.
    tags_col: a column that contains a string like "dress summer floral pink"
              OR a list of tags. We'll treat it as text.

    Output: recs with updated 'final_score' and sorted descending.
    """
    fb = load_feedback()
    liked_ids = set(map(str, fb.get("likes", [])))
    disliked_ids = set(map(str, fb.get("dislikes", [])))

    # Join tags onto recommendations
    temp = recs.copy()
    temp[id_col] = temp[id_col].astype(str)

    cat = catalog.copy()
    cat[id_col] = cat[id_col].astype(str)

    temp = temp.merge(cat[[id_col, tags_col]], on=id_col, how="left")

    def tokenize(x):
        if x is None:
            return set()
        if isinstance(x, list):
            return set(map(str.lower, map(str, x)))
        return set(str(x).lower().split())

    # Build a preference profile from liked/disliked items
    liked_tags = set()
    disliked_tags = set()

    if len(liked_ids) > 0:
        liked_rows = cat[cat[id_col].isin(liked_ids)]
        for t in liked_rows[tags_col].tolist():
            liked_tags |= tokenize(t)

    if len(disliked_ids) > 0:
        disliked_rows = cat[cat[id_col].isin(disliked_ids)]
        for t in disliked_rows[tags_col].tolist():
            disliked_tags |= tokenize(t)

    # Score adjustment based on tag overlap
    final_scores: List[float] = []
    for _, row in temp.iterrows():
        base = float(row.get(base_score_col, 0.0))
        item_tags = tokenize(row.get(tags_col))

        like_overlap = len(item_tags & liked_tags)
        dislike_overlap = len(item_tags & disliked_tags)

        # Normalize overlap so it doesn't explode
        like_adj = min(1.0, like_overlap / 8.0) * like_boost
        dislike_adj = min(1.0, dislike_overlap / 8.0) * dislike_penalty

        final_scores.append(base + like_adj - dislike_adj)

    temp["final_score"] = final_scores
    temp = temp.sort_values("final_score", ascending=False).reset_index(drop=True)
    return temp
