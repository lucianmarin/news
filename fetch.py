import feedparser
import requests
import time
from dateutil.parser import parse
from helpers import fetch_desc, fetch_fb, get_url
from models import News
from settings import FEEDS


def grab_entries():
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
            n = News(link=url, title=entry.title)
            n.time = parse(entry.published).timestamp()
            n.author = getattr(entry, 'author', None)
            if n.time > time.time() - 48 * 3600:
                n.save()
                print(n.link)
        except Exception as e:
            pass
    return entries


def cleanup():
    q = News.query.filter(time=(None, time.time() - 48 * 3600))
    c = q.count()
    q.delete()
    print("Deleted {0} entries".format(c))


def grab_description():
    for entry in News.query.all():
        if entry.description is None:
            entry.description = fetch_desc(entry.link)
            entry.save()
            print(entry.link)
            print(entry.description)


def grab_facebook():
    is_allowed = True
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


grab_entries()
cleanup()
grab_description()
# grab_facebook()
