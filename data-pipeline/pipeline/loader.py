"""
============================================================
PIPELINE LAYER 3 — LOADER
============================================================
Role: Data Engineer

Responsibility: Take the CLEAN list of post dicts from transformer.py
and write them into the SQLite database using SQLAlchemy.

This layer does NOT know about Lobsters' JSON format and does NOT
do any network calls. It only saves or updates rows.
============================================================
"""

from pipeline.models import Post
from pipeline.db import get_session


def load_posts(posts: list) -> dict:
    """
    Saves a list of transformed post dicts into the database.
    Uses upsert logic: update existing posts, insert new ones.

    Args:
        posts (list[dict]): Clean post dicts from transformer.transform_posts()

    Returns:
        dict: Summary of what happened.
              Example: {"inserted": 7, "updated": 3, "total": 10}
    """

    session = get_session()

    inserted = 0
    updated = 0

    try:
        for post in posts:
            existing = (
                session.query(Post)
                .filter_by(post_id=post["post_id"])
                .first()
            )

            if existing:
                existing.score = post["score"]
                existing.num_comments = post["num_comments"]
                updated += 1

            else:
                new_post = Post(
                    post_id=post["post_id"],
                    title=post["title"],
                    author=post["author"],
                    score=post["score"],
                    num_comments=post["num_comments"],
                    url=post["url"],
                    permalink=post["permalink"],
                    created_utc=post["created_utc"],
                    fetched_at=post["fetched_at"],
                )

                session.add(new_post)
                inserted += 1

        session.commit()

        return {
            "inserted": inserted,
            "updated": updated,
            "total": len(posts),
        }

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()