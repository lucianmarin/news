import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from app.helpers import fetch_paragraphs
from app.models import Article


def top(request):
    distinct = Article.objects.exclude(shares=None).order_by('domain', '-shares').distinct('domain').values('id')
    index = Article.objects.filter(id__in=distinct).order_by('-shares')
    return HttpResponse(
        json.dumps(list(index.values())),
        content_type="application/json"
    )


def recent(request):
    distinct = Article.objects.order_by('domain', '-pub').distinct('domain').values('id')
    index = Article.objects.filter(id__in=distinct).order_by('-pub').values()
    return HttpResponse(
        json.dumps(list(index.values())),
        content_type="application/json"
    )


def story(request, id):
    article = get_object_or_404(Article, id=id)
    item = list(Article.objects.filter(id=id).values())[0]
    item['paragraphs'] = fetch_paragraphs(article.url)
    return HttpResponse(
        json.dumps(item),
        content_type="application/json"
    )
