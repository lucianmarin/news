from werkzeug.contrib.cache import FileSystemCache

cache = FileSystemCache('./cache')

magazines = ['http://feeds.arstechnica.com/arstechnica/index/',
             'http://feeds.macrumors.com/MacRumors-Front',
             'http://feeds.feedburner.com/d0od',
             'http://feeds.feedburner.com/sub/9to5mac',
             'http://feeds.feedburner.com/sub/anandtech',
             'http://feeds.feedburner.com/sub/engadget',
             'http://feeds.feedburner.com/sub/gsmarena',
             'http://feeds.feedburner.com/sub/nautilus',
             'http://feeds.feedburner.com/sub/recode',
             'http://feeds.feedburner.com/sub/techcrunch',
             'http://feeds.feedburner.com/sub/verge']

news = ['https://news.ycombinator.com/rss',
        'https://lobste.rs/rss',
        'https://bitmia.com/rss']

feeds = magazines + news
