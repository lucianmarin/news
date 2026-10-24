#!/usr/bin/env python
import asyncio
from datetime import datetime, timezone
from statistics import mean

import aiohttp
import feedparser
from dateutil.parser import parse
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tortoise import Tortoise

from app.filters import hostname, sitename
from app.helpers import get_url, get_description, md5
from app.models import Article
from app.settings import FEEDS, TORTOISE_ORM


class ArticleFetcher:
    @property
    def now(self):
        return datetime.now(timezone.utc).timestamp()

    @property
    def cutoff(self):
        return self.now - 48 * 3600

    def entry_to_article(self, entry):
        try:
            link = entry.get('feedburner_origlink') or entry.get('link')
            if not link:
                return None
            url = get_url(link)
            published = parse(entry.published).timestamp()
            if not self.now > published > self.cutoff:
                return None
            return Article(
                id=md5(url),
                url=url,
                title=entry.title,
                domain=hostname(url),
                site=sitename(url),
                pub=published,
                author=entry.get('author', ''),
                description=get_description(entry),
            )
        except Exception as e:
            print(f"Error preparing {entry.get('link', '<unknown>')}: {e}")
            return None

    async def insert_entries(self, entries):
        articles = {}
        for entry in entries:
            article = self.entry_to_article(entry)
            if article is not None:
                articles[article.id] = article

        if not articles:
            return

        # One upsert per batch instead of a SELECT + INSERT/UPDATE per entry.
        await Article.bulk_create(
            articles.values(),
            update_fields=[
                'url', 'title', 'domain', 'site', 'pub', 'author', 'description'
            ],
            on_conflict=['id'],
        )
        for article in articles.values():
            print('Processed', article.url)

    async def get_entries(self, session, feed):
        try:
            async with session.get(feed, timeout=10) as response:
                text = await response.text()
            print(f"Fetched {feed}")
            return feedparser.parse(text).entries
        except Exception as e:
            print(f"Error fetching {feed}: {e}")
            return []

    async def grab_entries(self):
        entries = []
        async with aiohttp.ClientSession() as session:
            results = await asyncio.gather(
                *(self.get_entries(session, feed) for feed in FEEDS),
                return_exceptions=True,
            )
        for result in results:
            if isinstance(result, Exception):
                print(f"Error collecting feed entries: {result}")
                continue
            entries.extend(result)
        await self.insert_entries(entries)

    async def cleanup(self):
        deleted_count = await Article.filter(pub__lt=self.cutoff).delete()
        print(f"Deleted {deleted_count} entries")

    async def grab_score(self):
        articles = await Article.all()
        if not articles:
            return

        titles = [a.title.strip() for a in articles]
        descriptions = [a.description.strip() if a.description else "" for a in articles]

        title_vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')
        desc_vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')

        title_matrix = title_vectorizer.fit_transform(titles) * 2.0
        desc_matrix = desc_vectorizer.fit_transform(descriptions)

        tfidf_matrix = hstack([title_matrix, desc_matrix])
        cos_sim = cosine_similarity(tfidf_matrix)

        for i, article in enumerate(articles):
            similarities = [cos_sim[i][j] for j in range(len(articles)) if j != i]
            article.score = mean(similarities) * 10 if similarities else 0

        await Article.bulk_update(articles, fields=['score'], batch_size=500)
        for article in articles:
            print(f"{article.score:.4f} {article.title}")


async def main():
    await Tortoise.init(config=TORTOISE_ORM)
    try:
        fetcher = ArticleFetcher()
        await fetcher.grab_entries()
        await fetcher.cleanup()
        await fetcher.grab_score()
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(main())
