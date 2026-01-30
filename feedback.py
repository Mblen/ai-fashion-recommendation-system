import json
import os
from typing import Dict, List

FEEDBACK_PATH = os.path.join("data", "feedback.json")

def _ensure_feedback_file() -> None:
    os.makedirs(os.path.dirname(FEEDBACK_PATH), exist_ok=True)
    if not os.path.exists(FEEDBACK_PATH):
        with open(FEEDBACK_PATH, "w", encoding="utf-8") as f:
            json.dump({"likes": [], "dislikes": []}, f, indent=2)

def load_feedback() -> Dict[str, List[str]]:
    _ensure_feedback_file()
    with open(FEEDBACK_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_feedback(data: Dict[str, List[str]]) -> None:
    _ensure_feedback_file()
    with open(FEEDBACK_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def add_feedback(item_id: str, liked: bool) -> None:
    """
    Stores feedback persistently.
    item_id should be a stable identifier (string) for the recommended item.
    """
    data = load_feedback()
    likes = set(map(str, data.get("likes", [])))
    dislikes = set(map(str, data.get("dislikes", [])))

    item_id = str(item_id)

    if liked:
        likes.add(item_id)
        dislikes.discard(item_id)
    else:
        dislikes.add(item_id)
        likes.discard(item_id)

    data["likes"] = sorted(likes)
    data["dislikes"] = sorted(dislikes)
    save_feedback(data)
