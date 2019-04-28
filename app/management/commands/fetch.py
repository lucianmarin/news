import feedparser
import requests
import time
from dateutil.parser import parse
from django.core.management.base import BaseCommand
from app.filters import hostname
from app.helpers import get_url, fetch_desc, fetch_fb
from app.models import Article
from news.settings import FEEDS


class Command(BaseCommand):
    help = "Fetch articles from feeds."

    def grab_entries(self):
        entries = []
        for feed in FEEDS:
            r = requests.get(feed)
            entries += feedparser.parse(r.text).entries
            print(feed)
        for entry in entries:
            try:
                orig = entry.get('feedburner_origlink', '')
                entry.link = orig if orig else entry.link
                url = get_url(entry.link)
                published = parse(entry.published).timestamp()
                if published > time.time() - 48 * 3600:
                    article, is_created = Article.objects.get_or_create(
                        url=url,
                        title=entry.title,
                        domain=hostname(url),
                        pub=published,
                        author=getattr(entry, 'author', '')
                    )
            except Exception as e:
                pass
        return entries

    def cleanup(self):
        q = Article.objects.filter(pub__lt=time.time() - 48 * 3600)
        c = q.count()
        q.delete()
        print("Deleted {0} entries".format(c))

    def grab_description(self):
        for article in Article.objects.filter(
            description=None
        ).order_by('-id'):
            article.description = fetch_desc(article.url)
            article.save(update_fields=['description'])
            print(article.url)
            print(article.description)

    def grab_facebook(self):
        is_allowed = True
        articles = Article.objects.filter(
            has_fb=False,
            pub__lt=time.time() - 8 * 3600
        ).order_by('id')
        for article in articles:
            if is_allowed:
                fb = fetch_fb(article.url)
                if 'error' in fb:
                    is_allowed = False
                    print('error')
                else:
                    engagement = fb.get('engagement', {})
                    article.comments = engagement.get('comment_count', 0)
                    article.reactions = engagement.get('reaction_count', 0)
                    article.shares = engagement.get('share_count', 0)
                    article.save(update_fields=['comments, reactions, shares'])
                    print(article.comments, article.reactions, article.shares)

    def handle(self, *args, **options):
        self.grab_entries()
        self.cleanup()
        self.grab_description()
        self.grab_facebook()
