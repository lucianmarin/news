from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemBytecodeCache, FileSystemLoader

from app.filters import hostname, shortdate, sitename, superscript, truncate
from app.helpers import load_articles
from app.local import DEBUG

app = FastAPI()
env = Environment(
    loader=FileSystemLoader("templates"),
    bytecode_cache=FileSystemBytecodeCache(),
    enable_async=True
)
env.filters['hostname'] = hostname
env.filters['sitename'] = sitename
env.filters['shortdate'] = shortdate
env.filters['superscript'] = superscript
env.filters['truncate'] = truncate
env.globals['brand'] = "Hotnews"
env.globals['v'] = 14

if DEBUG:
    app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def hot_resource(request: Request, p: int = 1):
    articles_data = load_articles()
    articles_list = list(articles_data.values())

    # Pagination
    page = p if p > 0 else 1
    limit = 10
    offset = limit * (page - 1)
    domains = set(a['domain'] for a in articles_list)
    count = len(domains)
    pages = (count + limit - 1) // limit  # ceil(count / limit)

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

    entries = distinct_entries[offset:offset + limit]

    content = await env.get_template("main.html").render_async({
        "request": request,
        "entries": entries,
        "page": page,
        "pages": pages,
        "view": 'hottest'
    })
    return HTMLResponse(content)


@app.get("/cold")
async def cold_resource(request: Request, p: int = 1):
    articles_data = load_articles()
    articles_list = list(articles_data.values())

    # Pagination
    page = p if p > 0 else 1
    limit = 10
    offset = limit * (page - 1)
    domains = set(a['domain'] for a in articles_list)
    count = len(domains)
    pages = (count + limit - 1) // limit  # ceil(count / limit)

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

    entries = distinct_entries[offset:offset + limit]

    content = await env.get_template("main.html").render_async({
        "request": request,
        "entries": entries,
        "page": page,
        "pages": pages,
        "view": 'coldest'
    })
    return HTMLResponse(content)


@app.get("/new")
async def new_resource(request: Request, p: int = 1):
    articles_data = load_articles()
    articles_list = list(articles_data.values())

    # Pagination
    page = p if p > 0 else 1
    limit = 10
    offset = limit * (page - 1)
    domains = set(a['domain'] for a in articles_list)
    count = len(domains)
    pages = (count + limit - 1) // limit  # ceil(count / limit)

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

    entries = distinct_entries[offset:offset + limit]

    content = await env.get_template("main.html").render_async({
        "request": request,
        "entries": entries,
        "page": page,
        "pages": pages,
        "view": 'newest'
    })
    return HTMLResponse(content)


@app.get("/{site}")
async def site_resource(site: str, request: Request, p: int = 1):
    articles_data = load_articles()
    articles_list = [v for v in articles_data.values() if v['site'] == site]

    # Pagination
    page = p if p > 0 else 1
    limit = 10
    offset = limit * (page - 1)
    count = len(articles_list)
    pages = (count + limit - 1) // limit  # ceil(count / limit)

    articles_list.sort(key=lambda x: x['pub'])
    articles_list.sort(key=lambda x: x['score'], reverse=True)

    entries = articles_list[offset:offset + limit]

    content = await env.get_template("site.html").render_async({
        "request": request,
        "entries": entries,
        "site": site,
        "page": page,
        "pages": pages,
        "view": 'site'
    })
    return HTMLResponse(content)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
