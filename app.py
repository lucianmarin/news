import feedparser
import requests
from flask import Flask, jsonify, render_template, request
from helpers import fetch_paragraphs
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
    return render_template('main.html', entries=entries, count=count,
                           view='home')


@app.route('/recent/')
def recent():
    count = News.query.count()
    entries = News.query.order_by('-time').limit(0, 15).execute()
    return render_template('main.html', entries=entries, count=count,
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
    paragraphs = fetch_paragraphs(article.link)
    return render_template('text.html', entry=article, lines=paragraphs, count=count)
