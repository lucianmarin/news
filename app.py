import feedparser
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, render_template, request
from filters import hostname, date, shortdate
from models import News

app = Flask('newscafe')

app.jinja_env.filters['hostname'] = hostname
app.jinja_env.filters['date'] = date
app.jinja_env.filters['shortdate'] = shortdate
app.jinja_env.globals['v'] = 5


@app.route('/api/0/newscafe/')
def api_popular():
    entries = News.query.order_by('-shares').limit(0, 15).execute()
    dicts = []
    for entry in entries:
        dicts.append(entry.to_dict())
    return jsonify(dicts)


@app.route('/api/0/recent/')
def api_recent():
    entries = News.query.order_by('-time').limit(0, 15).execute()
    dicts = []
    for entry in entries:
        dicts.append(entry.to_dict())
    return jsonify(dicts)


@app.route('/')
def home():
    count = News.query.count()
    entries = News.query.order_by('-shares').limit(0, 15).execute()
    return render_template('base.html', entries=entries, count=count,
                           view='home')


@app.route('/recent/')
def recent():
    count = News.query.count()
    entries = News.query.order_by('-time').limit(0, 15).execute()
    return render_template('base.html', entries=entries, count=count,
                           view='last')


@app.route('/about/')
def about():
    return render_template('about.html', view='about')


@app.route('/debug/')
def debug():
    url = request.args.get('url', '')
    entries = feedparser.parse(requests.get(url).content).entries
    return jsonify(entries)


@app.route('/text/<id>/')
def text(id):
    count = News.query.count()
    article = News.get(id)
    r = requests.get(article.link, headers={
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Safari/605.1.15",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    })
    soup = BeautifulSoup(r.content, features="lxml")
    candidate = None
    count = 0
    for tag in soup.findAll():
        length = len(tag.findAll('p', recursive=False))
        if length > count:
            candidate = tag
            count = length
    paragraphs = []
    if candidate:
        for child in candidate.children:
            if child.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                text = child.text.strip()
                if text:
                    paragraphs.append(text)
    return render_template('text.html', entry=article, lines=paragraphs, count=count)
