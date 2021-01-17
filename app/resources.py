from falcon import status_codes
from falcon.errors import HTTPNotFound

from app.helpers import fetch_paragraphs
from app.jinja import env
from app.models import Article


class StaticResource(object):
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
            resp.body = f.read()


class MainResource:
    def ids(self, mode):
        return Article.objects.order_by('domain', mode).distinct('domain').values('id')

    def on_get(self, req, resp):
        articles = Article.objects.count()
        sites = Article.objects.distinct('domain').count()

        breaking = Article.objects.filter(id__in=self.ids('-score')).order_by('-score')
        current = Article.objects.filter(id__in=self.ids('-pub')).order_by('-pub')

        template = env.get_template('pages/main.html')
        resp.body = template.render(
            breaking=breaking[:24], current=current[:24],
            articles=articles, sites=sites, view='main'
        )


class ReadResource:
    def on_get(self, req, resp, base):
        articles = Article.objects.filter(id=int(base, 36))
        if not articles:
            raise HTTPNotFound()

        article = articles[0]
        article.description = None
        lines = fetch_paragraphs(article.url)

        template = env.get_template('pages/read.html')
        resp.body = template.render(
            article=article, lines=lines, view='read'
        )


class AboutResource:
    def on_get(self, req, resp):
        count = Article.objects.count()
        sites = Article.objects.order_by('domain').distinct('domain').values_list('domain', flat=True)
        template = env.get_template('pages/about.html')
        resp.body = template.render(
            sites=sites, count=count, view='about'
        )
