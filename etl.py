import requests
from db import setup_database, insert_post, insert_rejected

API_URL = "https://jsonplaceholder.typicode.com/posts"


# ── EXTRACT ──────────────────────────────────────────────────────────────────

def extract():
    """Fetch all posts from the public API."""
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    data = response.json()
    print(f"[EXTRACT] Fetched {len(data)} records from API.")
    return data


# ── TRANSFORM ─────────────────────────────────────────────────────────────────

def validate_and_transform(record):
    """
    Apply validation and transformation rules to a single record.

    Returns:
        (transformed_record, None)  on success
        (None, reason_string)       on failure
    """
    # Rule 1: Required fields must be present and non-empty
    for field in ("userId", "id", "title", "body"):
        if record.get(field) is None or record.get(field) == "":
            return None, f"Missing or empty field: '{field}'"

    title = str(record["title"]).strip()
    body = str(record["body"]).strip()

    # Rule 2: Title length between 3 and 100 characters
    if not (3 <= len(title) <= 100):
        return None, f"Title length {len(title)} out of range [3, 100]"

    # Rule 3: Body must have at least 5 words
    word_count = len(body.split())
    if word_count < 5:
        return None, f"Body too short: only {word_count} word(s)"

    transformed = {
        "id": int(record["id"]),
        "user_id": int(record["userId"]),
        "title": title,
        "body": body,
        "word_count": word_count,
    }
    return transformed, None


def transform(raw_records):
    """Run all records through validation and transformation."""
    valid = []
    rejected = []

    for record in raw_records:
        result, reason = validate_and_transform(record)
        if result:
            valid.append(result)
        else:
            rejected.append((record, reason))

    print(f"[TRANSFORM] {len(valid)} records passed validation. "
          f"{len(rejected)} records rejected.")
    return valid, rejected


# ── LOAD ──────────────────────────────────────────────────────────────────────

def load(valid_records, rejected_records):
    """Insert valid and rejected records into the database."""
    for post in valid_records:
        insert_post(post)
    print(f"[LOAD] Inserted {len(valid_records)} records into 'posts' table.")

    for raw, reason in rejected_records:
        insert_rejected(raw, reason)
    if rejected_records:
        print(f"[LOAD] Inserted {len(rejected_records)} rejected records "
              f"into 'rejected_records' table.")


# ── MAIN ──────────────────────────────────────────────────────────────────────

def run_pipeline():
    setup_database()

    raw = extract()
    valid, rejected = transform(raw)
    load(valid, rejected)

    print("Pipeline complete.")


if __name__ == "__main__":
    run_pipeline()