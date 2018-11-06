import feedparser
import requests
from flask import Flask, jsonify, render_template, request
from filters import hostname, date, shortdate
from helpers import load_db, hours_ago
from models import News

app = Flask('newscafe')

app.jinja_env.filters['hostname'] = hostname
app.jinja_env.filters['date'] = date
app.jinja_env.filters['shortdate'] = shortdate
app.jinja_env.globals['v'] = 4


@app.route('/api/0/newscafe/')
def api_popular():
    data = load_db()
    entries = sorted(data.values(), key=lambda k: k['shares'] if 'shares' in k else 0, reverse=True)
    return jsonify(entries[:15])


@app.route('/api/0/recent/')
def api_recent():
    data = load_db()
    entries = sorted(data.values(), key=lambda k: k['time'], reverse=True)
    return jsonify(entries[:15])


@app.route('/')
def home():
    # data = load_db()
    # entries = sorted(data.values(), key=lambda k: k['shares'] if 'shares' in k else 0, reverse=True)
    # count = len(entries)
    # entries = entries[:15]
    count = News.query.count()
    entries = News.query.order_by('-shares').limit(0, 15).execute()
    return render_template('base.html', entries=entries,
                           count=count, view='home')


@app.route('/recent/')
def recent():
    # data = load_db()
    # entries = sorted(data.values(), key=lambda k: k['time'], reverse=True)
    # count = len(entries)
    # entries = entries[:15]
    count = News.query.count()
    entries = News.query.order_by('-time').limit(0, 15).execute()
    return render_template('base.html', entries=entries,
                           count=count, view='last')


@app.route('/about/')
def about():
    return render_template('about.html', view='about')


@app.route('/debug/')
def debug():
    url = request.args.get('url', '')
    if url:
        entries = feedparser.parse(requests.get(url).content).entries
    else:
        data = load_db()
        no_past_shares = [v for v in data.values() if 'shares' not in v and v['time'] < hours_ago()]
        no_past_description = [v for v in data.values() if 'description' not in v and v['time'] < hours_ago()]
        no_recent_shares = [v for v in data.values() if 'shares' not in v and v['time'] > hours_ago()]
        no_recent_description = [v for v in data.values() if 'description' not in v and v['time'] > hours_ago()]
        entries = {
            'no past shares': len(no_past_shares),
            'no past description': len(no_past_description),
            'no recent shares': len(no_recent_shares),
            'no recent description': len(no_recent_description)
        }
    return jsonify(entries)
