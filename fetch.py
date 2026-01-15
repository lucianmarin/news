#!/usr/bin/env python
from datetime import datetime, timezone

import feedparser
import requests
from dateutil.parser import parse
from sentence_transformers import SentenceTransformer
import numpy as np

from app.filters import hostname
from app.helpers import fetch_content, get_url, load_articles, save_articles, md5
from app.settings import FEEDS


class ArticleFetcher:
    def __init__(self):
        self.ignored = [
            "https://kottke.org/quick-links"
        ]
        self.articles = {}

    @property
    def now(self):
        return datetime.now(timezone.utc).timestamp()

    @property
    def cutoff(self):
        return self.now - 48 * 3600

    def get_entries(self, feed):
        try:
            r = requests.get(feed)
            print(feed)
            entries = feedparser.parse(r.text).entries
            print(len(entries), "entries found")
            for entry in entries:
                try:
                    origlink = entry.get('feedburner_origlink')
                    entry.link = origlink if origlink else entry.link
                    url = get_url(entry.link)
                    published = parse(entry.published).timestamp()
                    if self.now > published > self.cutoff and url not in self.ignored:
                        key = md5(url)
                        if key not in self.articles:
                            self.articles[key] = {
                                'id': key,
                                'base': key,
                                'url': url,
                                'title': entry.title,
                                'domain': hostname(url),
                                'pub': published,
                                'author': getattr(entry, 'author', ''),
                                'description': None,
                                'score': 0,
                                'paragraphs': []
                            }
                            print('Created', url)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(f"Error processing feed {feed}: {e}")

    def grab_entries(self):
        for feed in FEEDS:
            self.get_entries(feed)

    def cleanup(self):
        keys_to_delete = [k for k, v in self.articles.items() if v['pub'] < self.cutoff]
        for k in keys_to_delete:
            del self.articles[k]
        print("Deleted {0} entries".format(len(keys_to_delete)))

    def grab_score(self):
        keys_to_fetch = [k for k, v in self.articles.items()]
        titles = [v['title'].strip() for v in self.articles.values()]
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model.encode(titles)
        for i, key in enumerate(keys_to_fetch):
            similarities = np.dot(embeddings, embeddings[i])
            similarities[i] = 0  # exclude self
            score = np.mean(similarities) if len(similarities) > 1 else 0
            self.articles[key]['score'] = float(score)
            print(score, self.articles[key]['title'])

    def get_content(self, key):
        article = self.articles[key]
        try:
            description, paragraphs = fetch_content(article['url'])
            if key in self.articles:
                self.articles[key]['description'] = description
                self.articles[key]['paragraphs'] = paragraphs
                print('Read', article['url'], len(paragraphs))
                print(article['description'])
        except Exception as e:
            print(f"Error fetching content for {article.get('url')}: {e}")

    def grab_content(self):
        keys_to_fetch = [k for k, v in self.articles.items() if not v.get('description')]
        for key in keys_to_fetch:
            self.get_content(key)


if __name__ == "__main__":
    fetcher = ArticleFetcher()
    fetcher.articles = load_articles()
    fetcher.grab_entries()
    fetcher.cleanup()
    fetcher.grab_score()
    fetcher.grab_content()
    save_articles(fetcher.articles)
