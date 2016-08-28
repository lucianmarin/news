import datetime
import feedparser
import json
import requests
import time
import urllib

from config import feeds
from werkzeug.contrib.cache import MemcachedCache

cache = MemcachedCache(['127.0.0.1:11211'])
total = 0


for feed in feeds:
    print('Fetching', feed)
    start = datetime.datetime.utcnow()
    response = requests.get(feed)
    items = feedparser.parse(response.content).entries
    newitems = []
    for item in items:
        newitem = {}
        redirect = requests.head(item.link, allow_redirects=True)
        newitem['link'] = urllib.parse.urljoin(redirect.url, urllib.parse.urlparse(redirect.url).path)
        graph = 'https://graph.facebook.com/v2.7/?id=' + urllib.parse.quote(newitem['link']) + '&access_token=531212323670365|wzDqeYsX6vQhiebyAr7PofFxCf0'
        facebook = json.loads(requests.get(graph).text)
        newitem['facebook'] = {'shares': 0, 'description': ''}
        try:
            newitem['facebook']['shares'] = facebook['share']['share_count']
        except:
            pass
        try:
            newitem['facebook']['description'] = facebook['og_object']['description']
        except:
            pass
        newitem['elapsed'] = redirect.elapsed.total_seconds()
        newitem['time'] = time.mktime(item.published_parsed) + 7200
        newitem['author'] = item.get('author', '')
        newitem['published'] = item.get('published', '')
        newitem['title'] = item.get('title', '')
        newitems.append(newitem)
    end = datetime.datetime.utcnow()
    total += (end - start).total_seconds()
    print('Time', (end - start).seconds, 'seconds')
    cache.set(feed, newitems, timeout=3600)


print('Total', round(total/60, 2), 'minutes')
