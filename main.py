from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import FileSystemBytecodeCache

from app.filters import hostname, shortdate, sitename, superscript, truncate
from app.helpers import load_articles
from app.local import DEBUG

app = FastAPI()
templates = Jinja2Templates(directory="templates")
templates.env.auto_reload = DEBUG
templates.env.bytecode_cache = FileSystemBytecodeCache()
templates.env.filters['hostname'] = hostname
templates.env.filters['sitename'] = sitename
templates.env.filters['shortdate'] = shortdate
templates.env.filters['superscript'] = superscript
templates.env.filters['truncate'] = truncate
templates.env.globals['brand'] = "News"
templates.env.globals['v'] = 12

if DEBUG:
    app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def hot_resource(request: Request):
    articles_data = load_articles()
    articles_list = list(articles_data.values())

    articles_count = len(articles_list)
    domains = set(a['domain'] for a in articles_list)
    sites_count = len(domains)
    limit = sites_count // 2

    # Order by domain, -score, pub to mimic distinct(domain) behavior logic
    # Python sort is stable, so we sort in reverse order of importance:
    # 1. pub (asc)
    # 2. score (desc)
    # 3. domain
    articles_list.sort(key=lambda x: x['pub'])
    articles_list.sort(key=lambda x: x['score'], reverse=True)
    articles_list.sort(key=lambda x: x['domain'])

    distinct_entries = []
    seen_domains = set()
    for a in articles_list:
        if a['domain'] not in seen_domains:
            distinct_entries.append(a)
            seen_domains.add(a['domain'])

    # Now order by -score, pub
    distinct_entries.sort(key=lambda x: x['pub'])
    distinct_entries.sort(key=lambda x: x['score'], reverse=True)

    entries = distinct_entries[:limit]

    return templates.TemplateResponse("pages/main.html", {
        "request": request,
        "entries": entries,
        "articles": articles_count,
        "sites": sites_count,
        "view": 'hottest'
    })


@app.get("/cold")
async def cold_resource(request: Request):
    articles_data = load_articles()
    articles_list = list(articles_data.values())

    articles_count = len(articles_list)
    domains = set(a['domain'] for a in articles_list)
    sites_count = len(domains)
    limit = sites_count // 2

    # Order by domain, -score, pub to mimic distinct(domain) behavior logic
    # Python sort is stable, so we sort in reverse order of importance:
    # 1. pub (asc)
    # 2. score (desc)
    # 3. domain
    articles_list.sort(key=lambda x: x['pub'])
    articles_list.sort(key=lambda x: x['score'])
    articles_list.sort(key=lambda x: x['domain'])

    distinct_entries = []
    seen_domains = set()
    for a in articles_list:
        if a['domain'] not in seen_domains:
            distinct_entries.append(a)
            seen_domains.add(a['domain'])

    # Now order by -score, pub
    distinct_entries.sort(key=lambda x: x['pub'])
    distinct_entries.sort(key=lambda x: x['score'])

    entries = distinct_entries[:limit]

    return templates.TemplateResponse("pages/main.html", {
        "request": request,
        "entries": entries,
        "articles": articles_count,
        "sites": sites_count,
        "view": 'coldest'
    })


@app.get("/new")
async def new_resource(request: Request):
    articles_data = load_articles()
    articles_list = list(articles_data.values())

    articles_count = len(articles_list)
    domains = set(a['domain'] for a in articles_list)
    sites_count = len(domains)
    limit = sites_count // 2

    # Order by domain, -pub to mimic distinct(domain)
    # Sort keys in reverse importance:
    # 1. pub (desc)
    # 2. domain
    articles_list.sort(key=lambda x: x['pub'], reverse=True)
    articles_list.sort(key=lambda x: x['domain'])

    distinct_entries = []
    seen_domains = set()
    for a in articles_list:
        if a['domain'] not in seen_domains:
            distinct_entries.append(a)
            seen_domains.add(a['domain'])

    # Order by -pub
    distinct_entries.sort(key=lambda x: x['pub'], reverse=True)

    entries = distinct_entries[:limit]

    return templates.TemplateResponse("pages/main.html", {
        "request": request,
        "entries": entries,
        "articles": articles_count,
        "sites": sites_count,
        "view": 'newest'
    })


@app.get("/{site}")
async def site_resource(site: str, request: Request):
    articles_data = load_articles()
    articles_list = [v for v in articles_data.values() if v['site'] == site]

    articles_list.sort(key=lambda x: x['pub'])
    articles_list.sort(key=lambda x: x['score'], reverse=True)

    return templates.TemplateResponse("pages/site.html", {
        "request": request,
        "entries": articles_list,
        "site": site,
        "view": 'site'
    })


@app.get("/about")
async def about_resource(request: Request):
    articles = load_articles()
    count = len(articles)
    sites = sorted(list(set(a['domain'] for a in articles.values())))

    return templates.TemplateResponse("pages/about.html", {
        "request": request,
        "sites": sites,
        "count": count,
        "view": 'about'
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
