import datetime
import feedparser
import json
import requests
import urllib

from config import feeds
from flask import Flask, jsonify, redirect, render_template, request
from werkzeug.contrib.cache import MemcachedCache

app = Flask('subfeeder')
cache = MemcachedCache(['127.0.0.1:11211'])


def get_entries():
    entries = []
    for feed in feeds:
        entries += cache.get(feed) or []
    return entries


@app.route('/debug')
def debug():
    url = request.args.get('url', '')
    if url:
        entries = feedparser.parse(requests.get(url).content).entries
    else:
        entries = []
    return jsonify(entries)


@app.route('/api')
def api():
    entries = get_entries()
    return jsonify(entries)


@app.route('/')
def home():
    entries = get_entries()
    count = len(entries)
    entries = sorted(entries, key=lambda k: k['facebook']['shares'], reverse=True)
    verbose = request.cookies.get('verbose', 'true')
    verbose = json.loads(verbose)

    if verbose:
        entries = entries[:15]
    else:
        entries = entries[:25]

    return render_template('base.html', entries=entries, count=count, verbose=verbose, view='home')


@app.route('/recent')
def recent():
    entries = get_entries()
    count = len(entries)
    entries = sorted(entries, key=lambda k: k['time'], reverse=True)
    verbose = request.cookies.get('verbose', 'true')
    verbose = json.loads(verbose)

    if verbose:
        entries = entries[:15]
    else:
        entries = entries[:25]

    return render_template('base.html', entries=entries, count=count, verbose=verbose, view='last')


@app.route('/succinct')
def set_succinct():
    go_back = redirect(request.referrer or '/')
    response = app.make_response(go_back)
    response.set_cookie('verbose', value='false', max_age=365*24*3600)
    return response


@app.route('/verbose')
def set_verbose():
    go_back = redirect(request.referrer or '/')
    response = app.make_response(go_back)
    response.set_cookie('verbose', value='true', max_age=365*24*3600)
    return response


@app.template_filter('hostname')
def filter_hostname(value):
    ''' Get hostname from an url '''
    url = urllib.parse.urlsplit(value)
    return url.netloc.replace('www.', '')


@app.template_filter('date')
def filter_date(struct):
    timestamp = datetime.datetime.fromtimestamp(struct)
    return timestamp.strftime('%b %-e, %Y %H:%M')


@app.template_filter('shortdate')
def filter_shortdate(struct):
    ''' Short time interval for a timestamp '''
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


app.run(debug=True)
