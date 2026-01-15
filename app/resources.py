from falcon import status_codes
from falcon.errors import HTTPNotFound

from app.jinja import env
from app.helpers import load_articles


class StaticResource:
    binary = ['png', 'jpg', 'woff', 'woff2']
    mime_types = {
        'js': "application/javascript",
        'json': "application/json",
        'css': "text/css",
        'woff': "font/woff",
        'woff2': "font/woff2",
        'png': "image/png",
        'jpg': "image/jpeg"
    }

    def on_get(self, req, resp, filename):
        print("load", filename)
        name, ext = filename.split('.')
        mode = 'rb' if ext in self.binary else 'r'
        resp.status = status_codes.HTTP_200
        resp.content_type = self.mime_types[ext]
        resp.cache_control = ["max-age=3600000"]
        with open(f'static/{filename}', mode) as f:
            resp.text = f.read()


class BreakingResource:
    def on_get(self, req, resp):
        articles_data = load_articles()
        articles_list = list(articles_data.values())

        articles_count = len(articles_list)
        domains = set(a['domain'] for a in articles_list)
        sites_count = len(domains)
        limit = sites_count // 2

        # Order by domain, -score, pub to mimic distinct(domain) behavior logic
        # Python sort is stable, so we sort in reverse order of importance:
        # 1. pub (asc)
        # 2. score (desc)
        # 3. domain
        articles_list.sort(key=lambda x: x['pub'])
        articles_list.sort(key=lambda x: x['score'], reverse=True)
        articles_list.sort(key=lambda x: x['domain'])

        distinct_entries = []
        seen_domains = set()
        for a in articles_list:
            if a['domain'] not in seen_domains:
                distinct_entries.append(a)
                seen_domains.add(a['domain'])

        # Now order by -score, pub
        distinct_entries.sort(key=lambda x: x['pub'])
        distinct_entries.sort(key=lambda x: x['score'], reverse=True)

        entries = distinct_entries[:limit]

        template = env.get_template('pages/main.html')
        resp.text = template.render(
            entries=entries,
            articles=articles_count, sites=sites_count, view='breaking'
        )


class CurrentResource:
    def on_get(self, req, resp):
        articles_data = load_articles()
        articles_list = list(articles_data.values())

        articles_count = len(articles_list)
        domains = set(a['domain'] for a in articles_list)
        sites_count = len(domains)
        limit = sites_count // 2

        # Order by domain, -pub to mimic distinct(domain)
        # Sort keys in reverse importance:
        # 1. pub (desc)
        # 2. domain
        articles_list.sort(key=lambda x: x['pub'], reverse=True)
        articles_list.sort(key=lambda x: x['domain'])

        distinct_entries = []
        seen_domains = set()
        for a in articles_list:
            if a['domain'] not in seen_domains:
                distinct_entries.append(a)
                seen_domains.add(a['domain'])

        # Order by -pub
        distinct_entries.sort(key=lambda x: x['pub'], reverse=True)

        entries = distinct_entries[:limit]

        template = env.get_template('pages/main.html')
        resp.text = template.render(
            entries=entries,
            articles=articles_count, sites=sites_count, view='current'
        )


class ReadResource:
    def on_get(self, req, resp, base):
        articles = load_articles()
        entry = articles.get(base)

        if not entry:
            raise HTTPNotFound()

        template = env.get_template('pages/read.html')
        resp.text = template.render(
            entry=entry, view='read'
        )


class AboutResource:
    def on_get(self, req, resp):
        articles = load_articles()
        count = len(articles)
        sites = sorted(list(set(a['domain'] for a in articles.values())))
        template = env.get_template('pages/about.html')
        resp.text = template.render(
            sites=sites, count=count, view='about'
        )
