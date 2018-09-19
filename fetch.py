import feedparser
import requests
import urllib

from helpers import feeds, load_db, save_db, to_date

token = "531212323670365|wzDqeYsX6vQhiebyAr7PofFxCf0"
api_path = "https://graph.facebook.com/v2.8/?id={0}&access_token={1}"

data = load_db()

entries = []
for feed in feeds:
    response = requests.get(feed)
    entries += feedparser.parse(response.content).entries
    print(feed)

for entry in entries:
    if entry.link not in data:
        print(entry.link)
        item = {
            'link': entry.link,
            'time': to_date(entry.published_parsed).timestamp(),
            'published': to_date(entry.published_parsed).isoformat(),
            'author': entry.get('author', ''),
            'title': entry.get('title', '')
        }
        data[entry.link] = item

allowed = True
temp = data
for key in temp.keys():
    if allowed and ('shares' or 'description') not in data[key]:
        url = urllib.parse.quote(entry.link)
        graph = api_path.format(url, token)
        facebook = requests.get(graph).json()
        if 'error' in facebook:
            allowed = False
        elif facebook:
            if 'share' in facebook and 'share_count' in facebook['share']:
                data[key]['shares'] = int(facebook['share']['share_count'])
            else:
                data[key]['shares'] = 0
            if 'og_object' in facebook and 'description' in facebook['og_object']:
                data[key]['description'] = facebook['og_object']['description']
            else:
                data[key]['description'] = ''
        print(facebook)

print(len(data.values()))

save_db(data)
