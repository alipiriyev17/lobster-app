"""
============================================================
PIPELINE LAYER 2 — TRANSFORMER
============================================================
Role: Data Engineer

Responsibility: Take the RAW Lobsters JSON from fetcher.py and turn
it into a clean list of dictionaries that match our database schema.

This layer does NOT touch the internet and does NOT touch the database.
============================================================
"""

from datetime import datetime, timezone


def transform_post(raw_post_data: dict) -> dict:
    """
    Transforms one raw Lobsters post into our database format.
    """

    parsed_date = datetime.fromisoformat(raw_post_data["created_at"])
    created_utc = parsed_date.timestamp()

    submitter_user = raw_post_data.get("submitter_user", "unknown")

    if isinstance(submitter_user, dict):
        author = submitter_user.get("username", "unknown")
    else:
        author = submitter_user

    return {
        "post_id": raw_post_data["short_id"],
        "title": raw_post_data["title"],
        "author": author,
        "score": raw_post_data["score"],
        "num_comments": raw_post_data["comment_count"],
        "url": raw_post_data.get("url") or raw_post_data.get("comments_url") or "",
        "permalink": raw_post_data["comments_url"],
        "created_utc": created_utc,
        "fetched_at": datetime.now(timezone.utc),
    }


def transform_posts(raw_json: list, limit: int = 10) -> list:
    """
    Transforms the full raw Lobsters response into a list of clean posts.
    Keeps only the first `limit` posts.
    """

    return [transform_post(post) for post in raw_json[:limit]]