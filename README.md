# Simple ETL Pipeline

A beginner-to-intermediate Python project demonstrating a complete ETL (Extract, Transform, Load) workflow. It pulls data from a public API, applies validation and transformation rules, and stores the results in a local SQLite database.

## What It Does

- **Extract** – Fetches posts data from [JSONPlaceholder](https://jsonplaceholder.typicode.com/), a free public REST API
- **Transform** – Cleans and validates each record (title length, non-null checks, word count)
- **Load** – Inserts valid records into a SQLite database; logs rejected records separately

## Project Structure

```
simple-etl-pipeline/
├── README.md
├── etl.py          # Main ETL script
├── db.py           # Database setup and helpers
├── requirements.txt
```

## Requirements

- Python 3.8+
- `requests` library

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Pipeline

```bash
python etl.py
```

After running, you'll see console output summarizing how many records were loaded or rejected. A file called `posts.db` will be created in the project directory.

## Querying the Results

Open the database with the built-in SQLite CLI:

```bash
sqlite3 posts.db
```

Then try:

```sql
SELECT * FROM posts LIMIT 5;
SELECT COUNT(*) FROM posts;
SELECT * FROM rejected_records;
```

## Transformation Rules

| Rule | Description |
|---|---|
| Non-null check | `userId`, `id`, `title`, and `body` must all be present |
| Title length | Title must be between 3 and 100 characters |
| Body word count | Body must contain at least 5 words |
| Title cleaning | Leading/trailing whitespace is stripped from title and body |

## Skills Demonstrated

- Python scripting and project structure
- REST API consumption with `requests`
- Data validation and transformation logic
- SQL schema design and parameterized inserts with `sqlite3`
- ETL pipeline architecture (separation of concerns across modules)

## Example Output

```
[EXTRACT] Fetched 100 records from API.
[TRANSFORM] 97 records passed validation. 3 records rejected.
[LOAD] Inserted 97 records into 'posts' table.
[LOAD] Inserted 3 rejected records into 'rejected_records' table.
Pipeline complete.
```