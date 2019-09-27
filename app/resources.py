from falcon import MEDIA_HTML, HTTPNotFound
from app.helpers import fetch_paragraphs
from app.jinja import env
from app.models import Article


class MainResource:
    def on_get(self, req, resp):
        count = Article.objects.count()
        distinct = Article.objects.order_by('domain', '-score').distinct('domain').values('id')
        articles = Article.objects.filter(id__in=distinct).order_by('-score')

        template = env.get_template('pages/index.html')
        resp.content_type = MEDIA_HTML
        resp.body = template.render(
            articles=articles[:15], count=count, view='index'
        )


class RecentResource:
    def on_get(self, req, resp):
        count = Article.objects.count()
        distinct = Article.objects.order_by('domain', '-pub').distinct('domain').values('id')
        articles = Article.objects.filter(id__in=distinct).order_by('-pub')

        template = env.get_template('pages/index.html')
        resp.content_type = MEDIA_HTML
        resp.body = template.render(
            articles=articles[:15], count=count, view='recent'
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
