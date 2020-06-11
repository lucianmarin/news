from falcon import HTTP_200
from falcon.constants import MEDIA_HTML
from falcon.errors import HTTPNotFound

from app.helpers import fetch_paragraphs
from app.jinja import env
from app.models import Article


class StaticResource(object):
    mime_types = {
        'json': "application/json",
        'css': "text/css",
        'woff': "font/woff",
        'png': "image/png",
        'jpg': "image/jpeg"
    }
    binary = ['png', 'jpg', 'woff']

    def on_get(self, req, resp, filename):
        print(filename)
        # do some sanity check on the filename
        name, ext = filename.split('.')
        mode = 'rb' if ext in self.binary else 'r'
        resp.status = HTTP_200
        resp.content_type = self.mime_types[ext]
        with open(f'static/{filename}', mode) as f:
            resp.body = f.read()


class MainResource:
    def on_get(self, req, resp):
        count = Article.objects.count()
        distinct = Article.objects.order_by('domain', '-score').distinct('domain').values('id')
        articles = Article.objects.filter(id__in=distinct).order_by('-score')
        template = env.get_template('pages/index.html')
        resp.content_type = MEDIA_HTML
        resp.body = template.render(
            articles=articles[:15], count=count, view='breaking'
        )


class RecentResource:
    def on_get(self, req, resp):
        count = Article.objects.count()
        distinct = Article.objects.order_by('domain', '-pub').distinct('domain').values('id')
        articles = Article.objects.filter(id__in=distinct).order_by('-pub')
        template = env.get_template('pages/index.html')
        resp.content_type = MEDIA_HTML
        resp.body = template.render(
            articles=articles[:15], count=count, view='current'
        )


class ReadResource:
    def on_get(self, req, resp, id):
        count = Article.objects.count()
        articles = Article.objects.filter(id=id)
        if not articles:
            raise HTTPNotFound()
        article = articles[0]
        article.description = None
        lines = fetch_paragraphs(article.url)
        template = env.get_template('pages/read.html')
        resp.content_type = MEDIA_HTML
        resp.body = template.render(
            article=article, lines=lines, count=count, view='read'
        )


class AboutResource:
    def on_get(self, req, resp):
        count = Article.objects.count()
        sites = Article.objects.order_by('domain').distinct('domain').values_list('domain', flat=True)
        template = env.get_template('pages/about.html')
        resp.content_type = MEDIA_HTML
        resp.body = template.render(
            sites=sites, count=count, view='about'
        )
