#!/usr/bin/env python
import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from dateutil.parser import parse
from statistics import mean

import feedparser
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tortoise import Tortoise

from app.filters import hostname, sitename
from app.helpers import get_url, get_description, md5
from app.settings import FEEDS, TORTOISE_ORM
from app.models import Article


class ArticleFetcher:
    @property
    def now(self):
        return datetime.now(timezone.utc).timestamp()

    @property
    def cutoff(self):
        return self.now - 48 * 3600

    async def insert_entry(self, entry):
        try:
            origlink = entry.get('feedburner_origlink')
            entry.link = origlink if origlink else entry.link
            url = get_url(entry.link)
            published = parse(entry.published).timestamp()
            key = md5(url)
            if self.now > published > self.cutoff:
                await Article.update_or_create(
                    id=key,
                    defaults={
                        'url': url,
                        'title': entry.title,
                        'domain': hostname(url),
                        'site': sitename(url),
                        'pub': published,
                        'author': entry.get('author', ''),
                        'description': get_description(entry),
                    }
                )
                print('Processed', url)
        except Exception as e:
            print(f"Error inserting {entry.link}: {e}")

    def get_entries(self, feed):
        print(f"Fetching {feed}")
        try:
            r = requests.get(feed, timeout=10)
            return feedparser.parse(r.text).entries
        except Exception as e:
            print(f"Error fetching {feed}: {e}")
            return []

    async def grab_entries(self):
        entries = []
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(self.get_entries, f): f for f in FEEDS}
            for future in as_completed(futures):
                entries.extend(future.result())
        for entry in entries:
            await self.insert_entry(entry)

    async def cleanup(self):
        deleted_count = await Article.filter(pub__lt=self.cutoff).delete()
        print(f"Deleted {deleted_count} entries")

    async def grab_score(self):
        articles = await Article.all()
        if not articles:
            return

        titles = [a.title.strip() for a in articles]
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(titles)
        cos_sim = cosine_similarity(tfidf_matrix)

        for i, article in enumerate(articles):
            similarities = [cos_sim[i][j] for j in range(len(titles)) if j != i]
            article.score = mean(similarities) if similarities else 0
            await article.save(update_fields=['score'])
            print(f"{article.score:.4f} {article.title}")


async def main():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

    fetcher = ArticleFetcher()
    await fetcher.grab_entries()
    await fetcher.cleanup()
    await fetcher.grab_score()

    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(main())
