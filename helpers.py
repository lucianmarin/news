import datetime
import ujson

feeds = ['http://feeds.feedburner.com/sub/daringfireball',
      'http://feeds.arstechnica.com/arstechnica/index/',
      'http://feeds.macrumors.com/MacRumors-Front',
      'http://feeds.feedburner.com/d0od',
      'http://feeds.feedburner.com/sub/9to5mac',
      'http://feeds.feedburner.com/sub/anandtech',
      'http://feeds.feedburner.com/sub/electrek',
      'http://feeds.feedburner.com/sub/engadget',
      'http://feeds.feedburner.com/sub/gsmarena',
      'http://feeds.feedburner.com/sub/nautilus',
      'http://feeds.feedburner.com/sub/recode',
      'http://feeds.feedburner.com/sub/techcrunch',
      'http://feeds.feedburner.com/sub/verge',
      'https://news.ycombinator.com/rss',
      'https://lobste.rs/rss']


def to_date(s):
    return datetime.datetime(s.tm_year, s.tm_mon, s.tm_mday, s.tm_hour, s.tm_min, s.tm_sec, tzinfo=datetime.timezone.utc)


def load_db():
    with open("db.json", "r") as db_file:
        return ujson.loads(db_file.read())


def save_db(data):
    week_ago = datetime.datetime.now() - datetime.timedelta(days=3)
    past_time = week_ago.timestamp()
    new = {}
    for link in data:
        if data[link]['time'] > past_time:
            new[link] = data[link]
    with open("db.json", "w") as db_file:
        return db_file.write(ujson.dumps(new, indent=2))
