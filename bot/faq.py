"""FAQ utilities for the Telegram bot."""
from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict, Optional

_FAQ_DATA: List[Dict[str, str]] = []


def _load_data() -> None:
    """Load FAQ data from the JSON file."""
    global _FAQ_DATA  # pylint: disable=global-statement
    if _FAQ_DATA:
        return
    faq_path = Path(__file__).resolve().parents[1] / "data" / "faq.json"
    with faq_path.open("r", encoding="utf-8") as f:
        _FAQ_DATA = json.load(f)


def find_answer(query: str) -> Optional[str]:
    """Return the best matching answer for the query."""
    _load_data()
    query_tokens = set(query.lower().split())
    best_answer = None
    best_score = 0
    for item in _FAQ_DATA:
        question_tokens = set(item["question"].lower().split())
        score = len(query_tokens & question_tokens)
        if score > best_score:
            best_score = score
            best_answer = item["answer"]
    if best_score == 0:
        return None
    return best_answer
