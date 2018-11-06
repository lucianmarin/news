import ujson
from datetime import datetime, timedelta, timezone


feeds = ['http://feeds.feedburner.com/sub/daringfireball',
         'http://feeds.arstechnica.com/arstechnica/index/',
         'http://feeds.macrumors.com/MacRumors-Front',
         'http://feeds.feedburner.com/sub/9to5google',
         'http://feeds.feedburner.com/sub/9to5mac',
         'http://feeds.feedburner.com/sub/anandtech',
         'http://feeds.feedburner.com/sub/electrek',
         'http://feeds.feedburner.com/sub/engadget',
         'http://feeds.feedburner.com/sub/gsmarena',
         'http://feeds.feedburner.com/sub/nautilus',
         'http://feeds.feedburner.com/sub/techcrunch',
         'http://feeds.feedburner.com/sub/verge',
         'https://news.ycombinator.com/rss',
         'https://lobste.rs/rss']


def hours_ago():
    return (datetime.utcnow() - timedelta(hours=12)).timestamp()


def days_ago():
    return (datetime.utcnow() - timedelta(hours=48)).timestamp()


def to_date(s):
    return datetime(s.tm_year, s.tm_mon, s.tm_mday, s.tm_hour, s.tm_min, s.tm_sec, tzinfo=timezone.utc)


def load_db():
    with open('db.json', 'r') as db_file:
        data = db_file.read()
    return ujson.loads(data)


def save_db(data):
    new = {}
    for key in data.keys():
        if data[key]['time'] > days_ago():
            new[key] = data[key]
    with open('db.json', 'w') as db_file:
        db_file.write(ujson.dumps(new, indent=2))
    return new
