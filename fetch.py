#!/usr/bin/env python
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from dateutil.parser import parse

import feedparser
import numpy as np
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.filters import hostname, sitename
from app.helpers import get_url, get_description, load_articles, save_articles, md5
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

    def insert_entry(self, entry):
        try:
            origlink = entry.get('feedburner_origlink')
            entry.link = origlink if origlink else entry.link
            url = get_url(entry.link)
            published = parse(entry.published).timestamp()
            key = md5(url)
            if self.now > published > self.cutoff and url not in self.ignored and key not in self.articles:
                self.articles[key] = {
                    'url': url,
                    'title': entry.title,
                    'domain': hostname(url),
                    'site': sitename(url),
                    'pub': published,
                    'author': entry.get('author', ''),
                    'description': get_description(entry),
                    'score': 0
                }
                print('Created', url)
        except Exception as e:
            print(e)

    def get_entries(self, feed):
        print(feed)
        r = requests.get(feed)
        return feedparser.parse(r.text).entries

    def grab_entries(self):
        entries = []
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(self.get_entries, f): f for f in FEEDS}
            for future in as_completed(futures):
                entries.extend(future.result())
        for entry in entries:
            self.insert_entry(entry)

    def cleanup(self):
        keys_to_delete = [k for k, v in self.articles.items() if v['pub'] < self.cutoff]
        for k in keys_to_delete:
            del self.articles[k]
        print("Deleted {0} entries".format(len(keys_to_delete)))

    def grab_score(self):
        keys_to_fetch = [k for k, v in self.articles.items()]
        titles = [v['title'].strip() for v in self.articles.values()]
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(titles)
        cos_sim = cosine_similarity(tfidf_matrix)
        for i, key in enumerate(keys_to_fetch):
            similarities = [cos_sim[i][j] for j in range(len(titles)) if j != i]
            score = np.mean(similarities) if similarities else 0
            self.articles[key]['score'] = float(score)
            print(score, self.articles[key]['title'])


if __name__ == "__main__":
    fetcher = ArticleFetcher()
    fetcher.articles = load_articles()
    fetcher.grab_entries()
    fetcher.cleanup()
    fetcher.grab_score()
    save_articles(fetcher.articles)
