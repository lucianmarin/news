from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from app.helpers import fetch_paragraphs
from app.models import Article


def index(request):
    count = Article.objects.count()
    theme = request.COOKIES.get('theme', 'light')
    mode = request.COOKIES.get('mode', 'details')

    distinct = Article.objects.order_by('domain', '-score').distinct('domain').values('id')
    index = Article.objects.filter(id__in=distinct).order_by('-score')
    index_list = index[:15] if mode == 'details' else index[:30]

    return render(request, 'index.jinja', {
        'articles': index_list,
        'count': count,
        'mode': mode,
        'theme': theme,
        'view': 'index'
    })


def recent(request):
    count = Article.objects.count()
    theme = request.COOKIES.get('theme', 'light')
    mode = request.COOKIES.get('mode', 'details')

    distinct = Article.objects.order_by('domain', '-pub').distinct('domain').values('id')
    index = Article.objects.filter(id__in=distinct).order_by('-pub')
    index_list = index[:15] if mode == 'details' else index[:30]

    return render(request, 'index.jinja', {
        'articles': index_list,
        'count': count,
        'mode': mode,
        'theme': theme,
        'view': 'recent'
    })


def read(request, id):
    count = Article.objects.count()
    theme = request.COOKIES.get('theme', 'light')

    article = get_object_or_404(Article, id=id)
    article.description = None
    lines = fetch_paragraphs(article.url)

    return render(request, 'read.jinja', {
        'article': article,
        'count': count,
        'lines': lines,
        'mode': 'details',
        'theme': theme,
        'view': 'read'
    })


def about(request):
    count = Article.objects.count()
    theme = request.COOKIES.get('theme', 'light')

    sites = Article.objects.order_by('domain').distinct('domain').values_list('domain', flat=True)

    return render(request, 'about.jinja', {
        'count': count,
        'sites': sites,
        'mode': 'details',
        'theme': theme,
        'view': 'about'
    })


def site_index(request, domain):
    count = Article.objects.count()
    index = Article.objects.filter(domain=domain).exclude(shares=None).order_by('-shares')

    return render(request, 'site.jinja', {
        'articles': index[:15],
        'count': count,
        'domain': domain,
        'view': 'site_index'
    })


def site_recent(request, domain):
    count = Article.objects.count()
    index = Article.objects.filter(domain=domain).order_by('-pub')

    return render(request, 'site.jinja', {
        'articles': index[:15],
        'count': count,
        'domain': domain,
        'view': 'site_recent'
    })


def settings(request, name, value):
    ref = request.META.get('HTTP_REFERER', '/')
    response = HttpResponseRedirect(ref)
    response.set_cookie(name, value)
    return response
