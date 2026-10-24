from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db.sqlite3"

TORTOISE_ORM = {
    "connections": {"default": f"sqlite://{DB_PATH}"},
    "apps": {
        "models": {
            "models": ["app.models"],
            "default_connection": "default",
            "migrations": "app.migrations",
        },
    },
    # Tortoise ORM 1.0 changed the default from False to True. Keep it explicit.
    "use_tz": True,
}

FEEDS = [
    "http://feeds.arstechnica.com/arstechnica/index",
    "http://feeds.arstechnica.com/arstechnica/features",
    "http://feeds.hbr.org/harvardbusiness/",
    "http://feeds.macrumors.com/macrumors-front",
    "http://feeds.imore.com/theiphoneblog",
    "http://feeds.androidcentral.com/androidcentral",
    "http://feeds.windowscentral.com/wmexperts",
    "http://feeds.feedburner.com/businessinsider",
    "http://feeds.feedburner.com/fubiz",
    "http://feeds.feedburner.com/neowin-main",
    "http://feeds.feedburner.com/petapixel",
    "http://feeds.feedburner.com/thehackersnews",
    "http://feeds.feedburner.com/venturebeat/szyf",
    "http://rss.sciam.com/scientificamerican-global",
    "https://9to5google.com/feed/",
    "https://9to5mac.com/feed/",
    "https://aeon.co/feed.rss",
    "https://aestheticamagazine.com/feed",
    "https://www.androidauthority.com/feed/",
    "https://www.arenaev.com/rss-articles.php3",
    "https://www.theatlantic.com/feed/best-of/",
    "https://www.atlasobscura.com/feeds/latest",
    "https://api.axios.com/feed/top/",
    "https://bair.berkeley.edu/blog/feed.xml",
    "https://bgr.com/feed/",
    "https://www.comingsoon.net/feed",
    "https://theconversation.com/articles.atom?language=en",
    "https://crackberry.com/rss.xml",
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
    "https://futurism.com/feed",
    "http://www.gsmarena.com/rss-news-reviews.php3",
    "https://gizmodo.com/feed/",
    "https://spectrum.ieee.org/feeds/feed.rss",
    "http://feeds.kottke.org/main",
    "https://www.japantimes.co.jp/feed/topstories",
    "https://joshmitteldorf.scienceblog.com/feed/",
    "https://increment.com/feed.xml",
    "https://feed.infoq.com/",
    "https://www.lesswrong.com/feed.xml",
    "https://www.lifespan.io/feed/",
    "https://longreads.com/feed/",
    "https://feeds.macrumors.com/MacRumors-All",
    "https://massivesci.com/feed.xml",
    "http://news.mit.edu/rss/feed",
    "https://mspoweruser.com/feed/",
    "https://nautil.us/feed/",
    "https://feeds.npr.org/1001/rss.xml",
    "https://www.omgubuntu.co.uk/feed",
    "https://www.polygon.com/rss/index.xml",
    "https://www.popularmechanics.com/rss/all.xml",
    "https://api.quantamagazine.org/feed/",
    "https://qz.com/feed",
    "https://quillette.com/articles/rss/",
    "https://www.theregister.co.uk/headlines.atom",
    "https://www.sciencenews.org/feed",
    "https://seths.blog/rss",
    "https://singularityhub.com/feed/",
    "https://www.sixthtone.com/rss",
    "https://www.smashingmagazine.com/feed/",
    "https://spacenews.com/feed/",
    "https://techcrunch.com/feed/",
    "https://thegradient.pub/rss/",
    "https://tidbits.com/feed/",
    "https://www.theverge.com/rss/index.xml",
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
