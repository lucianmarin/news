from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

import feedparser
import requests
from app.filters import hostname
from app.helpers import fetch_content, fetch_fb, get_url
from app.models import Article
from dateutil.parser import parse
from django.core.management.base import BaseCommand
from project.settings import FEEDS


class Command(BaseCommand):
    help = "Fetch articles from feeds."
    cores = 4
    ignored = [
        "https://kottke.org/quick-links"
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-fb',
            action='store_true',
            help='Skip Facebook API calls',
        )

    @property
    def now(self):
        return datetime.now(timezone.utc).timestamp()

    def get_entries(self, feed):
        r = requests.get(feed)
        print(feed)
        entries = feedparser.parse(r.text).entries
        for entry in entries:
            try:
                origlink = entry.get('feedburner_origlink')
                entry.link = origlink if origlink else entry.link
                url = get_url(entry.link)
                published = parse(entry.published).timestamp()
                if self.now > published > self.now - 48 * 3600 and url not in self.ignored:
                    article, is_created = Article.objects.get_or_create(
                        url=url,
                        title=entry.title,
                        domain=hostname(url),
                        pub=published,
                        author=getattr(entry, 'author', '')
                    )
            except Exception as e:
                print(e)

    def grab_entries(self):
        with ThreadPoolExecutor(max_workers=self.cores) as executor:
            executor.map(self.get_entries, FEEDS)

    def cleanup(self):
        q = Article.objects.filter(pub__lt=self.now - 48 * 3600)
        c = q.count()
        q.delete()
        print("Deleted {0} entries".format(c))

    def get_content(self, article):
        description, paragraphs = fetch_content(article.url)
        article.description = description
        article.paragraphs = paragraphs
        article.save(update_fields=['description', 'paragraphs'])
        print(article.url, len(paragraphs))
        print(article.description)

    def grab_content(self):
        articles = Article.objects.filter(description=None).order_by('-id')
        with ThreadPoolExecutor(max_workers=self.cores) as executor:
            executor.map(self.get_content, articles)

    def get_facebook(self, article):
        fb = fetch_fb(article.url)
        if 'error' in fb:
            print('error')
            return
        else:
            engagement = fb.get('engagement', {})
            article.comments = engagement.get('comment_count', 0)
            article.reactions = engagement.get('reaction_count', 0)
            article.shares = engagement.get('share_count', 0)
            article.score = article.comments + article.reactions + article.shares
            article.has_fb = True
            article.save(update_fields=[
                'comments', 'reactions', 'shares', 'score', 'has_fb'
            ])
            print(article.url, article.score)

    def grab_facebook(self):
        articles = Article.objects.filter(
            has_fb=False, pub__lt=self.now - 12 * 3600
        ).order_by('id')
        with ThreadPoolExecutor(max_workers=self.cores) as executor:
            executor.map(self.get_facebook, articles)

    def handle(self, *args, **options):
        self.grab_entries()
        self.cleanup()
        self.grab_content()
        if not options['skip_fb']:
            self.grab_facebook()
