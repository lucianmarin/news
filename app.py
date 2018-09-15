import datetime
import feedparser
import requests
import urllib

from config import cache, feeds
from flask import Flask, jsonify, render_template, request

app = Flask('newscafe')


def get_entries():
    entries = []
    for feed in feeds:
        fdict = cache.get(feed) or {}
        entries += fdict.values()

    uniques = {}
    for entry in entries:
        uniques[entry['link']] = entry
    entries = uniques.values()

    week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    past_time = week_ago.timestamp()
    recent = []
    for entry in entries:
        if entry['time'] > past_time:
            recent.append(entry)

    return recent


@app.route('/debug')
def debug():
    url = request.args.get('url', '')
    if url:
        entries = feedparser.parse(requests.get(url).content).entries
    else:
        entries = []
    return jsonify(entries)


@app.route('/api/popular')
def api_popular():
    entries = sorted(get_entries(), key=lambda k: k['shares'], reverse=True)
    return jsonify(entries[:50])


@app.route('/api/recent')
def api_recent():
    entries = sorted(get_entries(), key=lambda k: k['time'], reverse=True)
    return jsonify(entries[:50])


@app.route('/')
def home():
    entries = sorted(get_entries(), key=lambda k: k['shares'] if 'shares' in k else 0, reverse=True)
    count = len(entries)

    return render_template('base.html', entries=entries[:15], count=count, view='home')


@app.route('/recent')
def recent():
    entries = sorted(get_entries(), key=lambda k: k['time'], reverse=True)[:15]
    count = len(entries)

    return render_template('base.html', entries=entries[:15], count=count, view='last')


@app.template_filter('hostname')
def filter_hostname(value):
    """Get hostname from an url."""
    url = urllib.parse.urlsplit(value)
    return url.netloc.replace('www.', '')


@app.template_filter('date')
def filter_date(struct):
    timestamp = datetime.datetime.fromtimestamp(struct)
    return timestamp.strftime('%b %-e, %Y %H:%M')


@app.template_filter('shortdate')
def filter_shortdate(struct):
    """Short time interval for a timestamp."""
    timestamp = datetime.datetime.utcfromtimestamp(struct)
    delta = datetime.datetime.utcnow() - timestamp

    miliseconds = abs(delta.microseconds) // 1000
    seconds = abs(delta.seconds)
    days = abs(delta.days) % 365
    years = abs(delta.days) // 365
    weeks = days // 7

    if not years and not days:
        if not seconds:
            return "%dms" % miliseconds
        elif seconds < 60:
            return "%ds" % seconds
        elif seconds < 3600:
            return "%dm" % (seconds // 60)
        else:
            return "%dh" % (seconds // 3600)
    elif not years:
        if not weeks:
            return "%dd" % days
        else:
            return "%dw" % weeks
    else:
        if not weeks and not days:
            return "%dy" % years
        elif not weeks:
            return "%dy, %dd" % (years, days)
        else:
            return "%dy, %dw" % (years, weeks)
