# Hotnews

Hotnews is a high-performance news aggregator built with **FastAPI** for serving web requests. It aggregates news from a curated list of RSS feeds, scores them based on title/description uniqueness (higher score means more similar articles), and presents them in a clean interface.

## Tech Stack

*   **Python**: 3.10+
*   **Web Framework**: [FastAPI](https://fastapi.tiangolo.com/) (for fast asynchronous HTTP handling)
*   **Templating**: [Jinja2](https://jinja.palletsprojects.com/)
*   **RSS Parsing**: `feedparser`
*   **Content Extraction**: `BeautifulSoup` (bs4) with lxml
*   **Scoring**: scikit-learn (TF-IDF vectorization + cosine similarity)
*   **ORM**: Tortoise ORM with aiosqlite (schema managed by migrations)
*   **Data Storage**: SQLite (`db.sqlite3`)
*   **Server**: Uvicorn (ASGI server)

## Features

*   **RSS Aggregation**: Fetches articles from a wide range of tech, science, and news sources (configured in `app/settings.py`).
*   **Article Scoring**: Scores articles based on title and description similarity using TF-IDF vectorization and cosine similarity.
*   **Cleanup**: Automatically removes articles older than 48 hours to keep the content fresh.
*   **Views**: Multiple views - hottest (lowest score), coldest (highest score), newest articles.

## Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd hotnews
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**
    ```bash
    tortoise -c app.settings.TORTOISE_ORM migrate
    ```

    If you already have a `db.sqlite3` that was created before migrations were
    introduced, baseline it once instead of running the schema creation:
    ```bash
    tortoise -c app.settings.TORTOISE_ORM migrate --fake
    ```

## Usage

### Running the Web Server

```bash
python main.py
```

The server will start on `http://127.0.0.1:8000`.

### Fetching News

To populate the data with the latest news, run the fetch script:

```bash
python fetch.py
```

This script will:
1.  Fetch entries from all configured RSS feeds.
2.  Clean up articles older than 48 hours.
3.  Calculate similarity scores for articles.

**Note:** Run this script periodically (e.g., via `cron` or a scheduler) to keep the news updated.

### Changing the schema

Tortoise ORM manages the database with migrations. After changing a model:

```bash
tortoise -c app.settings.TORTOISE_ORM makemigrations
tortoise -c app.settings.TORTOISE_ORM migrate
```

Do not use `generate_schemas()` in the application or fetch script; it is only
intended for throwaway/test databases.

### Routes

- `/` - Hottest articles (most unique titles)
- `/cold` - Coldest articles (least unique titles)
- `/new` - Newest articles

## Configuration

- **RSS Feeds**: Edit `app/settings.py` to add or remove RSS feeds in the `FEEDS` list.
- **Headers**: Update `HEADERS` in `app/settings.py` for web scraping requests.
