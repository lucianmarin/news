import feedparser
import requests
import urllib

from helpers import feeds, load_db, save_db, to_date, hours_ago, days_ago

token = "531212323670365|wzDqeYsX6vQhiebyAr7PofFxCf0"
api_path = "https://graph.facebook.com/v2.8/?id={0}&access_token={1}"
allowed = True

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

values = sorted(data.values(), key=lambda k: k['time'], reverse=True)
filtered = {v['link'] for v in values if v['time'] > hours_ago}
for key in filtered:
    if allowed:
        url = urllib.parse.quote(data[key]['link'])
        graph = api_path.format(url, token)
        if 'description' not in data[key]:
            fb = requests.get(graph).json()
            if 'error' in fb:
                allowed = False
            else:
                og_object = fb.get('og_object', {})
                data[key]['description'] = og_object.get('description', '')
            print(fb)

values = sorted(data.values(), key=lambda k: k['time'])
filtered = {v['link'] for v in values if v['time'] < hours_ago}
for key in filtered:
    if allowed:
        url = urllib.parse.quote(data[key]['link'])
        graph = api_path.format(url, token)
        if 'shares' not in data[key]:
            fb = requests.get(graph).json()
            if 'error' in fb:
                allowed = False
            else:
                share = fb.get('share', {})
                data[key]['shares'] = share.get('share_count', 0)
                og_object = fb.get('og_object', {})
                data[key]['description'] = og_object.get('description', '')
            print(fb)

print(len(data.keys()))

save_db(data)
