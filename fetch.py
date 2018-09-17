import datetime
import feedparser
import requests
import urllib

from config import cache, feeds

total = 0
token = '531212323670365|wzDqeYsX6vQhiebyAr7PofFxCf0'
week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
past_time = week_ago.timestamp()


def to_date(s):
    return datetime.datetime(s.tm_year, s.tm_mon, s.tm_mday, s.tm_hour, s.tm_min, s.tm_sec, tzinfo=datetime.timezone.utc)


for feed in feeds:
    print('Fetching {0}'.format(feed))
    start = datetime.datetime.utcnow()
    response = requests.get(feed)
    entries = feedparser.parse(response.content).entries
    items = {}
    feed_cache = cache.get(feed) or []
    for entry in entries:
        item = {
            'link': entry.link,
            'time': to_date(entry.published_parsed).timestamp(),
            'published': to_date(entry.published_parsed).isoformat(),
            'author': entry.get('author', ''),
            'title': entry.get('title', '')
        }
        if entry.link in feed_cache:
            if 'shares' in feed_cache[entry.link]:
                item['shares'] = feed_cache[entry.link]['shares']
            if 'description' in feed_cache[entry.link]:
                item['description'] = feed_cache[entry.link]['description']
        if item['time'] > past_time:
            url = urllib.parse.quote(entry.link)
            graph = 'https://graph.facebook.com/v2.7/?id={0}&access_token={1}'.format(url, token)
            facebook = requests.get(graph).json()
            try:
                if 'error' not in facebook:
                    if 'share' in facebook:
                        item['shares'] = facebook['share']['share_count']
                    else:
                        item['shares'] = 0
                    if 'og_object' in facebook:
                        item['description'] = facebook['og_object']['description']
                    else:
                        item['description'] = ''
                print(facebook)
            except Exception as e:
                print(e)
                pass
        items[entry.link] = item
    end = datetime.datetime.utcnow()
    current = (end - start).total_seconds()
    total += current
    print('Time {0} seconds'.format(current))
    cache.set(feed, items, timeout=0)


print('Total {0} minutes'.format(round(total / 60, 2)))
