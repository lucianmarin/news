import feedparser
import requests
import urllib
import time
from dateutil.parser import parse
from models import News
from settings import FEEDS, TOKEN


def fetch_fb(link):
    path = "https://graph.facebook.com/v2.8/?id={0}&access_token={1}"
    url = urllib.parse.quote(link)
    graph = path.format(url, TOKEN)
    return requests.get(graph).json()


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
        n.author = entry.get('author', None)
        n.save()
    except Exception as e:
        print(e)

# clean up
News.query.filter(time=(None, time.time() - 48 * 3600)).delete()

for entry in News.query.filter(time=(time.time() - 8 * 3600, None)):
    if is_allowed and entry.description is None:
        fb = fetch_fb(entry.link)
        if 'error' in fb:
            is_allowed = False
            print('error')
        else:
            og_object = fb.get('og_object', {})
            entry.description = og_object.get('description', '')
            entry.save()
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
            entry.comments = share.get('comment_count', 0)
            entry.shares = share.get('share_count', 0)
            entry.save()
            print(entry.shares, entry.comments)
