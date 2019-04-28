from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from app.helpers import fetch_paragraphs
from app.models import Article


def index(request):
    count = Article.objects.count()
    theme = 'dark' if request.COOKIES.get('theme') == 'dark' else 'light'

    distinct = Article.objects.order_by('domain', '-shares').distinct('domain').values('id')
    index = Article.objects.filter(id__in=distinct).order_by('-shares')

    return render(request, 'index.jinja', {
        'articles': index[:15],
        'count': count,
        'theme': theme,
        'view': 'index'
    })


def reacted(request):
    count = Article.objects.count()
    theme = 'dark' if request.COOKIES.get('theme') == 'dark' else 'light'

    distinct = Article.objects.order_by('domain', '-reactions').distinct('domain').values('id')
    index = Article.objects.filter(id__in=distinct).order_by('-reactions')

    return render(request, 'index.jinja', {
        'articles': index[:15],
        'count': count,
        'theme': theme,
        'view': 'reacted'
    })


def commented(request):
    count = Article.objects.count()
    theme = 'dark' if request.COOKIES.get('theme') == 'dark' else 'light'

    distinct = Article.objects.order_by('domain', '-comments').distinct('domain').values('id')
    index = Article.objects.filter(id__in=distinct).order_by('-comments')

    return render(request, 'index.jinja', {
        'articles': index[:15],
        'count': count,
        'theme': theme,
        'view': 'commented'
    })


def recent(request):
    count = Article.objects.count()
    theme = 'dark' if request.COOKIES.get('theme') == 'dark' else 'light'

    distinct = Article.objects.order_by('domain', '-pub').distinct('domain').values('id')
    index = Article.objects.filter(id__in=distinct).order_by('-pub')

    return render(request, 'index.jinja', {
        'articles': index[:15],
        'count': count,
        'theme': theme,
        'view': 'recent'
    })


def read(request, id):
    count = Article.objects.count()
    theme = 'dark' if request.COOKIES.get('theme') == 'dark' else 'light'

    article = get_object_or_404(Article, id=id)
    article.description = None
    lines = fetch_paragraphs(article.url)

    return render(request, 'read.jinja', {
        'article': article,
        'count': count,
        'lines': lines,
        'theme': theme,
        'view': 'read'
    })


def about(request):
    count = Article.objects.count()
    theme = 'dark' if request.COOKIES.get('theme') == 'dark' else 'light'

    sites = Article.objects.order_by('domain').distinct('domain').values_list('domain', flat=True)

    return render(request, 'about.jinja', {
        'count': count,
        'sites': sites,
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


def light(request):
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie('theme', 'light')
    return response


def dark(request):
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie('theme', 'dark')
    return response
