import json
import requests
import urllib
from config import feeds
from time import mktime

import feedparser
from werkzeug.contrib.cache import MemcachedCache

cache = MemcachedCache(['127.0.0.1:11211'])


for feed in feeds:
    print('Fetching', feed)
    response = requests.get(feed)
    items = feedparser.parse(response.content).entries
    for item in items:
        item['link'] = requests.head(item.link, allow_redirects=True).url
        item['link'] = urllib.parse.urljoin(item.link, urllib.parse.urlparse(item.link).path)
        print(item.link)
        graph = 'https://graph.facebook.com/v2.7/?id=' + urllib.parse.quote(item.link) + '&access_token=531212323670365|wzDqeYsX6vQhiebyAr7PofFxCf0'
        facebook = requests.get(graph)
        item['facebook'] = json.loads(facebook.text)
        if not 'share' in item['facebook']:
            item['facebook']['share'] = {}
            item['facebook']['share']['share_count'] = 0
        item['timed'] = mktime(item.published_parsed)
    cache.set(feed, items, timeout=3600)
