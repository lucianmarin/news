from django.shortcuts import get_object_or_404, render
from app.helpers import fetch_paragraphs
from app.models import Article


def index(request):
    distinct = Article.objects.exclude(shares=None).order_by('domain', '-shares').distinct('domain').values('id')
    index = Article.objects.filter(id__in=distinct).order_by('-shares')
    count = Article.objects.count()

    return render(request, 'index.jinja', {
        'articles': index[:15],
        'count': count,
        'view': 'index'
    })


def recent(request):
    distinct = Article.objects.order_by('domain', '-pub').distinct('domain').values('id')
    index = Article.objects.filter(id__in=distinct).order_by('-pub')
    count = Article.objects.count()

    return render(request, 'index.jinja', {
        'articles': index[:15],
        'count': count,
        'view': 'recent'
    })


def about(request):
    count = Article.objects.count()

    return render(request, 'about.jinja', {
        'count': count,
        'view': 'about'
    })


def text(request, id):
    article = get_object_or_404(Article, id=id)
    article.description = None
    lines = fetch_paragraphs(article.url)
    count = Article.objects.count()

    return render(request, 'text.jinja', {
        'article': article,
        'count': count,
        'lines': lines,
        'view': 'text'
    })
