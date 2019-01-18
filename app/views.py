from django.shortcuts import get_object_or_404, render
from app.helpers import fetch_paragraphs
from app.models import Article


def index(request):
    count = Article.objects.count()

    distinct = Article.objects.exclude(shares=None).order_by('domain', '-shares').distinct('domain').values('id')
    index = Article.objects.filter(id__in=distinct).order_by('-shares')

    return render(request, 'index.jinja', {
        'articles': index[:15],
        'count': count,
        'view': 'index'
    })


def recent(request):
    count = Article.objects.count()

    distinct = Article.objects.order_by('domain', '-pub').distinct('domain').values('id')
    index = Article.objects.filter(id__in=distinct).order_by('-pub')

    return render(request, 'index.jinja', {
        'articles': index[:15],
        'count': count,
        'view': 'recent'
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


def about(request):
    count = Article.objects.count()

    sites = Article.objects.order_by('domain').distinct('domain').values_list('domain', flat=True)

    return render(request, 'about.jinja', {
        'count': count,
        'sites': sites,
        'view': 'about'
    })


def story(request, id):
    count = Article.objects.count()

    article = get_object_or_404(Article, id=id)
    article.description = None
    lines = fetch_paragraphs(article.url)

    return render(request, 'story.jinja', {
        'article': article,
        'count': count,
        'lines': lines,
        'view': 'story'
    })
