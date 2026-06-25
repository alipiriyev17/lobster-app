"""
============================================================
PIPELINE LAYER 1 — FETCHER
============================================================
Role: Data Engineer

Responsibility: Talk to Lobsters' public JSON endpoint and return
the RAW response data.
============================================================
"""

import requests

USER_AGENT = "python:lobsters-top-posts-student-project:v1.0 (by /u/your_username_here)"

LOBSTERS_HOTTEST_URL = "https://lobste.rs/hottest.json"


def fetch_top_posts_raw(limit: int = 10) -> list:
    """
    Fetches the raw "hottest" stories JSON from Lobsters.

    Args:
        limit (int): How many stories we ultimately want to keep.
                     Trimming happens in transformer.py, not here.

    Returns:
        list: The raw parsed JSON response from Lobsters.
    """
    headers = {"User-Agent": USER_AGENT}

    response = requests.get(
        LOBSTERS_HOTTEST_URL,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    return response.json()