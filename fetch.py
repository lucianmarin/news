import feedparser
import requests
import urllib

from datetime import datetime, timedelta
from helpers import feeds, load_db, save_db, to_date

token = "531212323670365|wzDqeYsX6vQhiebyAr7PofFxCf0"
api_path = "https://graph.facebook.com/v2.8/?id={0}&access_token={1}"
hours_ago = (datetime.now() - timedelta(days=1)).timestamp()
days_ago = (datetime.now() - timedelta(days=3)).timestamp()

data = load_db()

entries = []
for feed in feeds:
    response = requests.get(feed)
    entries += feedparser.parse(response.content).entries
    print(feed)

for entry in entries:
    if entry.link not in data:
        item = {
            'link': entry.link,
            'time': to_date(entry.published_parsed).timestamp(),
            'published': to_date(entry.published_parsed).isoformat(),
            'author': entry.get('author', ''),
            'title': entry.get('title', '')
        }
        if item['time'] > days_ago:
            data[entry.link] = item
        else:
            print(item['time'], item['link'])

allowed = True
for key in data.keys():
    if allowed:
        url = urllib.parse.quote(data[key]['link'])
        graph = api_path.format(url, token)
        if 'description' not in data[key] and data[key]['time'] > hours_ago:
            facebook = requests.get(graph).json()
            if 'error' in facebook:
                allowed = False
            elif 'og_object' in facebook:
                og = facebook['og_object']
                data[key]['description'] = og.get('description', '')
            print(facebook)
        if 'shares' not in data[key] and data[key]['time'] < hours_ago:
            facebook = requests.get(graph).json()
            if 'error' in facebook:
                allowed = False
            elif 'share' in facebook:
                share = facebook['share']
                data[key]['shares'] = int(share.get('share_count', 0))
            print(facebook)

print(len(data.values()))

save_db(data)
