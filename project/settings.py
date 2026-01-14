from project.local import DEBUG

SECRET_KEY = '4^suh^yp2@jm!a!8snts8wb(y2kx4v482km5mnc^+topkpc*!p'
DEBUG = DEBUG

ALLOWED_HOSTS = []
INSTALLED_APPS = ['app', 'django_extensions', 'django.contrib.postgres']
MIDDLEWARE = []
TEMPLATES = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'news',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '',
        'PORT': '6432'
    }
}
AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = False
USE_TZ = False
USE_ETAGS = False

FEEDS = [
    "http://feeds.arstechnica.com/arstechnica/index",
    "http://feeds.arstechnica.com/arstechnica/features",
    "http://rss.sciam.com/scientificamerican-global",
    # "http://feeds.reuters.com/news/artsculture",
    # "http://feeds.reuters.com/reuters/businessNews",
    # "http://feeds.reuters.com/reuters/entertainment",
    # "http://feeds.reuters.com/reuters/environment",
    # "http://feeds.reuters.com/reuters/healthNews",
    # "http://feeds.reuters.com/reuters/oddlyEnoughNews",
    # "http://feeds.reuters.com/reuters/scienceNews",
    # "http://feeds.reuters.com/reuters/technologyNews",
    "http://feeds.hbr.org/harvardbusiness/",
    "http://feeds.macrumors.com/macrumors-front",
    "https://crackberry.com/rss.xml",
    "http://feeds.imore.com/theiphoneblog",
    "http://feeds.androidcentral.com/androidcentral",
    "http://feeds.windowscentral.com/wmexperts",
    # "http://feeds.feedburner.com/businessinsider",
    "http://feeds.feedburner.com/fubiz",
    "http://feeds.feedburner.com/neowin-main",
    "http://feeds.feedburner.com/petapixel",
    "http://feeds.feedburner.com/thehackersnews",
    "http://feeds.feedburner.com/venturebeat/szyf",
    "https://9to5google.com/feed/",
    "https://9to5mac.com/feed/",
    "https://aeon.co/feed.rss",
    "https://aestheticamagazine.com/feed",
    "https://www.androidauthority.com/feed/",
    # "https://www.arenaev.com/rss-articles.php3",
    "https://www.theatlantic.com/feed/best-of/",
    # "https://www.atlasobscura.com/feeds/latest",
    "https://api.axios.com/feed/top/",
    # "https://balkaninsight.com/feed",
    "https://bair.berkeley.edu/blog/feed.xml",
    "https://bgr.com/feed/",
    "https://www.comingsoon.net/feed",
    # "https://theconversation.com/global/articles.rss",
    "https://www.dailyartmagazine.com/feed/",
    "https://deepmind.com/blog/feed/basic/",
    "https://distill.pub/rss.xml",
    "https://www.eff.org/rss/updates.xml",
    "https://electrek.co/feed/",
    "https://endpts.com/feed/",
    "https://www.engadget.com/rss.xml",
    "https://www.fastcompany.com/latest/rss",
    "https://fs.blog/feed/",
    "http://www.fubiz.net/en/feed/",
    "http://www.gsmarena.com/rss-news-reviews.php3",
    "https://karpathy.github.io/feed.xml",
    "https://spectrum.ieee.org/feeds/feed.rss",
    # "http://feeds.kottke.org/main",
    "https://www.japantimes.co.jp/feed/topstories",
    "https://joshmitteldorf.scienceblog.com/feed/",
    "https://increment.com/feed.xml",
    "https://feed.infoq.com/",
    "https://www.lesswrong.com/feed.xml",
    # "https://liliputing.com/feed",
    "https://www.lifespan.io/feed/",
    "https://longreads.com/feed/",
    "https://feeds.macrumors.com/MacRumors-All",
    "https://massivesci.com/feed.xml",
    "http://news.mit.edu/rss/feed",
    "https://mspoweruser.com/feed/",
    "http://nautil.us/rss/all",
    "https://feeds.npr.org/1001/rss.xml",
    "https://www.omgubuntu.co.uk/feed",
    "https://peterattiamd.com/feed/",
    "https://www.polygon.com/rss/index.xml",
    "https://www.producthunt.com/feed",
    "https://api.quantamagazine.org/feed/",
    "https://qz.com/feed",
    "https://quillette.com/articles/rss/",
    "https://www.theregister.co.uk/headlines.atom",
    "https://www.sciencenews.org/feed",
    "https://semiaccurate.com/feed/",
    "https://seths.blog/rss",
    "https://singularityhub.com/feed/",
    "https://www.sixthtone.com/rss",
    "https://www.smashingmagazine.com/feed/",
    "https://spacenews.com/feed/",
    "https://techcrunch.com/feed/",
    "https://www.techmeme.com/feed.xml",
    "https://thefreethoughtproject.com/feed/",
    "https://thegradient.pub/rss/",
    "https://tidbits.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://www.vice.com/en_us/rss/",
    "https://www.vox.com/rss/index.xml",
    "https://www.wired.com/feed/rss",
    "https://www.windowslatest.com/feed/"
]

LINKS = [
    "https://daringfireball.net/feeds/main",
    "https://news.ycombinator.com/rss",
    "https://lobste.rs/rss",
    "http://monocle.io/feed",
    "https://www.designernews.co/?format=rss",
    "https://www.techmeme.com/feed.xml",
    "http://rss.slashdot.org/Slashdot/slashdotMain"
]

HEADERS = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}
