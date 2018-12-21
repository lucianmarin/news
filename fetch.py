import feedparser
import requests
import time
from dateutil.parser import parse
from helpers import fetch_desc, fetch_fb
from models import News
from settings import FEEDS


is_allowed = True
entries = []
for feed in FEEDS:
    response = requests.get(feed)
    entries += feedparser.parse(response.content).entries
    print(feed)

for entry in entries:
    try:
        n = News(link=entry.link, title=entry.title)
        n.time = parse(entry.published).timestamp()
        n.author = getattr(entry, 'author', None)
        n.save()
        print(n.link)
        print(n.author)
    except Exception as e:
        print(e)

# clean up
News.query.filter(time=(None, time.time() - 48 * 3600)).delete()

for entry in News.query.all():
    if entry.description is None:
        entry.description = fetch_desc(entry.link)
        entry.save()
        print(entry.link)
        print(entry.description)

for entry in News.query.filter(time=(None, time.time() - 8 * 3600)):
    if is_allowed and entry.shares is None:
        fb = fetch_fb(entry.link)
        if 'error' in fb:
            is_allowed = False
            print('error')
        else:
            og_object = fb.get('og_object', {})
            entry.description = og_object.get('description', '')
            share = fb.get('share', {})
            entry.shares = share.get('share_count', 0)
            entry.save()
            print(entry.shares)
