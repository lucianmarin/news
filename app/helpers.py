import urllib
import json
import hashlib
import os
from bs4 import BeautifulSoup

from app.settings import DATA_FILE


def md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()


def load_articles():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_articles(articles):
    with open(DATA_FILE, 'w') as f:
        json.dump(articles, f, indent=4)


def get_url(link):
    url = urllib.parse.urlparse(link)
    url_list = list(url)
    url_list[4] = ""
    return urllib.parse.urlunparse(url_list)


def get_description(entry):
    description = entry.get('description')
    if not description:
        description = entry.get('summary')
    if not description:
        description = ""
    soup = BeautifulSoup(description, features="lxml")
    lines = [l.strip() for l in soup.text.split('\n') if l.strip()]
    return lines[0]
