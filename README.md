# Hotnews

Hotnews is a high-performance news aggregator built with **FastAPI** for serving web requests. It aggregates news from a curated list of RSS feeds, scores them based on title uniqueness (lower score means more unique/hotter articles), and presents them in a clean interface.

## Tech Stack

*   **Web Framework**: [FastAPI](https://fastapi.tiangolo.com/) (for fast asynchronous HTTP handling)
*   **Templating**: [Jinja2](https://jinja.palletsprojects.com/)
*   **RSS Parsing**: `feedparser`
*   **Content Extraction**: `BeautifulSoup` (bs4) with lxml
*   **Scoring**: NumPy for similarity calculations
*   **Data Storage**: JSON file (`data/articles.json`)
*   **Server**: Uvicorn (ASGI server)
*   **Other Libraries**: python-dateutil, tldextract, user-agents

## Features

*   **RSS Aggregation**: Fetches articles from a wide range of tech, science, and news sources (configured in `app/settings.py`).
*   **Article Scoring**: Scores articles based on title similarity to other articles (using sequence matching and mean similarity score).
*   **Content Extraction**: Automatically fetches and extracts the main content/paragraphs of articles using BeautifulSoup.
*   **Cleanup**: Automatically removes articles older than 48 hours to keep the content fresh.
*   **Views**: Multiple views - hottest (lowest score), coldest (highest score), newest articles.
*   **Individual Article Reading**: Dedicated page to read full extracted content.
*   **About Page**: Lists all source sites and article count.

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

4.  **Data Directory:**
    The application stores articles in `data/articles.json`. Ensure the `data/` directory exists or it will be created automatically.

## Usage

### Running the Web Server

You can run the web server using `uvicorn`:

```bash
uvicorn main:app --reload
```

Or directly with Python:

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
4.  Fetch the full content for new articles.

**Note:** Run this script periodically (e.g., via `cron` or a scheduler) to keep the news updated.

### Routes

- `/` - Hottest articles (most unique titles)
- `/cold` - Coldest articles (least unique titles)
- `/new` - Newest articles
- `/read/{id}` - Read individual article
- `/about` - About page with stats

## Configuration

- **RSS Feeds**: Edit `app/settings.py` to add or remove RSS feeds in the `FEEDS` list.
- **Data File**: Change `DATA_FILE` in `app/settings.py` to modify the storage location.
- **Headers**: Update `HEADERS` for web scraping requests.
