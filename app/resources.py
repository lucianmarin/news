from falcon import status_codes
from falcon.errors import HTTPNotFound

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
        return Article.objects.order_by(
            'domain', mode
        ).distinct('domain').values('id')

    def on_get(self, req, resp):
        articles = Article.objects.count()
        sites = Article.objects.distinct('domain').count()
        limit = sites // 2

        breaking = Article.objects.filter(id__in=self.ids('pub')).order_by('pub')
        current = Article.objects.filter(id__in=self.ids('-pub')).order_by('-pub')

        template = env.get_template('pages/main.html')
        resp.body = template.render(
            breaking=breaking[:limit], current=current[:limit],
            articles=articles, sites=sites, view='main'
        )


class ReadResource:
    def on_get(self, req, resp, base):
        articles = Article.objects.filter(id=int(base, 36))
        if not articles:
            raise HTTPNotFound()

        template = env.get_template('pages/read.html')
        resp.body = template.render(
            article=articles[0], view='read'
        )


class AboutResource:
    def on_get(self, req, resp):
        count = Article.objects.count()
        sites = Article.objects.order_by('domain').distinct('domain').values_list('domain', flat=True)
        template = env.get_template('pages/about.html')
        resp.body = template.render(
            sites=sites, count=count, view='about'
        )
