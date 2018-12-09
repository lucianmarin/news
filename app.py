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
    article = News.get(id)
    r = requests.get(article.link)
    soup = BeautifulSoup(r.content, features="lxml")
    candidates = {}
    for p in soup.findAll('p'):
        key = p.parent.get('class', ['_'])[0]
        if key in candidates:
            candidates[key] += 1
        else:
            candidates[key] = 1
    sorted_candidates = sorted(candidates.items(), key=lambda kv: kv[1])
    sorted_candidates.reverse()
    container = sorted_candidates[0][0]
    c = soup.select_one("." + container)
    paragraphs = []
    if c:
        for child in c.children:
            if child.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                text = child.text.strip()
                if text:
                    paragraphs.append(text)
    # lines = [line.strip() for line in c.text.splitlines() if line.strip()]
    return render_template('text.html', entry=article, lines=paragraphs)
