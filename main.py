from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemBytecodeCache, FileSystemLoader
from tortoise.contrib.fastapi import register_tortoise
from tortoise.functions import Max, Min
from tortoise.expressions import Subquery, RawSQL

from app.filters import hostname, shortdate, sitename, superscript, truncate
from app.local import DEBUG
from app.settings import TORTOISE_ORM
from app.models import Article

LIMIT = 16
SQL = 'SELECT "id" FROM ({0}) GROUP BY "domain"'

app = FastAPI()
env = Environment(
    autoescape=True,
    auto_reload=DEBUG,
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
env.globals['v'] = 15

if DEBUG:
    app.mount("/static", StaticFiles(directory="static"), name="static")

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)

@app.get("/")
async def hot_resource(request: Request, p: int = 1):
    page = p if p > 0 else 1
    offset = LIMIT * (page - 1)

    order_by = ("-score", "pub")
    ordered = Article.all().order_by(*order_by).sql()
    max_ids = await Article.raw(SQL.format(ordered))
    count = len(max_ids)
    pages = (count + LIMIT - 1) // LIMIT

    entries = await Article.filter(id__in=max_ids).order_by(*order_by).offset(offset).limit(LIMIT)

    content = await env.get_template("base.html").render_async({
        "request": request,
        "entries": entries,
        "page": page,
        "pages": pages,
        "view": 'hottest'
    })
    return HTMLResponse(content)


@app.get("/cold")
async def cold_resource(request: Request, p: int = 1):
    page = p if p > 0 else 1
    offset = LIMIT * (page - 1)

    order_by = ("score", "pub")
    ordered = Article.all().order_by(*order_by).sql()
    max_ids = await Article.raw(SQL.format(ordered))
    count = len(max_ids)
    pages = (count + LIMIT - 1) // LIMIT

    entries = await Article.filter(id__in=max_ids).order_by(*order_by).offset(offset).limit(LIMIT)

    content = await env.get_template("base.html").render_async({
        "request": request,
        "entries": entries,
        "page": page,
        "pages": pages,
        "view": 'coldest'
    })
    return HTMLResponse(content)


@app.get("/new")
async def new_resource(request: Request, p: int = 1):
    page = p if p > 0 else 1
    offset = LIMIT * (page - 1)

    order_by = ("-pub",)
    ordered = Article.all().order_by(*order_by).sql()
    max_ids = await Article.raw(SQL.format(ordered))
    count = len(max_ids)
    pages = (count + LIMIT - 1) // LIMIT

    entries = await Article.filter(id__in=max_ids).order_by(*order_by).offset(offset).limit(LIMIT)

    content = await env.get_template("base.html").render_async({
        "request": request,
        "entries": entries,
        "page": page,
        "pages": pages,
        "view": 'newest'
    })
    return HTMLResponse(content)


@app.get("/{site}")
async def site_resource(site: str, request: Request, p: int = 1):
    page = p if p > 0 else 1
    offset = LIMIT * (page - 1)

    query = Article.filter(site=site)
    count = await query.count()
    pages = (count + LIMIT - 1) // LIMIT

    entries = await query.order_by("-score", "pub").offset(offset).limit(LIMIT)

    content = await env.get_template("base.html").render_async({
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
