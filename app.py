import feedparser
import requests

from filters import hostname, date, shortdate
from helpers import load_db, hours_ago
from flask import Flask, jsonify, render_template, request

app = Flask('newscafe')

app.jinja_env.filters['hostname'] = hostname
app.jinja_env.filters['date'] = date
app.jinja_env.filters['shortdate'] = shortdate


@app.route('/debug')
def debug():
    url = request.args.get('url', '')
    if url:
        entries = feedparser.parse(requests.get(url).content).entries
    else:
        data = load_db()
        no_shares = [v for v in data.values() if 'shares' not in v and v['time'] < hours_ago]
        no_description = [v for v in data.values() if 'description' not in v and v['time'] > hours_ago]
        entries = {
            'no shares': len(no_shares),
            'no description': len(no_description)
        }
    return jsonify(entries)


@app.route('/api/popular')
def api_popular():
    data = load_db()
    entries = sorted(data.values(), key=lambda k: k['shares'] if 'shares' in k else 0, reverse=True)
    return jsonify(entries[:50])


@app.route('/api/recent')
def api_recent():
    data = load_db()
    entries = sorted(data.values(), key=lambda k: k['time'], reverse=True)
    return jsonify(entries[:50])


@app.route('/')
def home():
    data = load_db()
    entries = sorted(data.values(), key=lambda k: k['shares'] if 'shares' in k else 0, reverse=True)
    count = len(entries)

    return render_template('base.html', entries=entries[:15], count=count, view='home')


@app.route('/recent')
def recent():
    data = load_db()
    entries = sorted(data.values(), key=lambda k: k['time'], reverse=True)
    count = len(entries)

    return render_template('base.html', entries=entries[:15], count=count, view='last')
