from datetime import datetime, timezone

import feedparser
import requests
from dateutil.parser import parse
from django.core.management.base import BaseCommand

from app.filters import hostname
from app.helpers import fetch_desc, fetch_fb, get_url
from app.models import Article
from project.settings import FEEDS


class Command(BaseCommand):
    help = "Fetch articles from feeds."

    def add_arguments(self, parser):
        # Positional arguments
        # parser.add_argument('poll_ids', nargs='+', type=int)

        # Named (optional) arguments
        parser.add_argument(
            '--skip-fb',
            action='store_true',
            help='Skip Facebook API calls',
        )

    def grab_entries(self):
        entries = []
        for feed in FEEDS:
            r = requests.get(feed)
            entries += feedparser.parse(r.text).entries
            print(feed)
        for entry in entries:
            try:
                origlink = entry.get('feedburner_origlink')
                entry.link = origlink if origlink else entry.link
                url = get_url(entry.link)
                published = parse(entry.published).timestamp()
                now = datetime.now(timezone.utc).timestamp()
                if now > published > now - 48 * 3600:
                    article, is_created = Article.objects.get_or_create(
                        url=url,
                        title=entry.title,
                        domain=hostname(url),
                        pub=published,
                        author=getattr(entry, 'author', '')
                    )
            except Exception as e:
                print(e)

    def cleanup(self):
        now = datetime.now(timezone.utc).timestamp()
        q = Article.objects.filter(pub__lt=now - 48 * 3600)
        c = q.count()
        q.delete()
        print("Deleted {0} entries".format(c))

    def grab_description(self):
        articles = Article.objects.filter(description=None).order_by('-id')
        for article in articles:
            article.description = fetch_desc(article.url)
            article.save(update_fields=['description'])
            print(article.url)
            print(article.description)

    def grab_facebook(self):
        now = datetime.now(timezone.utc).timestamp()
        articles = Article.objects.filter(
            has_fb=False, pub__lt=now - 12 * 3600
        ).order_by('id')
        for article in articles:
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
                article.save(update_fields=['comments', 'reactions', 'shares', 'score', 'has_fb'])
                print(article.url, article.score)

    def handle(self, *args, **options):
        # print(options)
        self.grab_entries()
        self.cleanup()
        self.grab_description()
        if not options['skip_fb']:
            self.grab_facebook()
