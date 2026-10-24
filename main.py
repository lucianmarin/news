from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemBytecodeCache, FileSystemLoader
from tortoise.contrib.fastapi import RegisterTortoise, tortoise_exception_handlers

from app.filters import hostname, shortdate, sitename, superscript
from app.local import DEBUG
from app.models import Article
from app.settings import TORTOISE_ORM

LIMIT = 10


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with RegisterTortoise(app, config=TORTOISE_ORM):
        yield


app = FastAPI(
    lifespan=lifespan,
    exception_handlers=tortoise_exception_handlers(),
)
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
env.globals['brand'] = "Hotnews"
env.globals['v'] = 18

if DEBUG:
    app.mount("/static", StaticFiles(directory="static"), name="static")


def current_page(p: int) -> tuple[int, int]:
    page = max(p, 1)
    return page, LIMIT * (page - 1)


async def top_entries(order_by: tuple[str, ...], page: int) -> tuple[list[Article], int]:
    """Return the first article per domain, in the requested order.

    SQLite has no ``DISTINCT ON``, so fetch lightweight ``(id, domain)``
    pairs in order and keep the first article for every domain. This is
    deterministic, unlike selecting a bare ``id`` with ``GROUP BY domain``.
    """
    _, offset = current_page(page)
    rows = await Article.all().order_by(*order_by).values_list("id", "domain")

    seen: set[str] = set()
    ids: list[str] = []
    for article_id, domain in rows:
        if domain not in seen:
            seen.add(domain)
            ids.append(article_id)

    page_ids = ids[offset:offset + LIMIT]
    entries = await Article.filter(id__in=page_ids).order_by(*order_by)
    return entries, len(ids)


async def render(request: Request, p: int, order_by: tuple[str, ...], view: str, **context):
    page, _ = current_page(p)
    entries, count = await top_entries(order_by, page)
    content = await env.get_template("base.html").render_async({
        "request": request,
        "entries": entries,
        "page": page,
        "pages": (count + LIMIT - 1) // LIMIT,
        "view": view,
        **context,
    })
    return HTMLResponse(content)


@app.get("/")
async def hot_resource(request: Request, p: int = 1):
    return await render(request, p, ("-score", "pub"), "hottest")


@app.get("/cold")
async def cold_resource(request: Request, p: int = 1):
    return await render(request, p, ("score", "pub"), "coldest")


@app.get("/new")
async def new_resource(request: Request, p: int = 1):
    return await render(request, p, ("-pub",), "newest")


@app.get("/{site}")
async def site_resource(site: str, request: Request, p: int = 1):
    page, offset = current_page(p)
    query = Article.filter(site=site)
    count = await query.count()
    entries = await query.order_by("-score", "pub").offset(offset).limit(LIMIT)

    content = await env.get_template("base.html").render_async({
        "request": request,
        "entries": entries,
        "site": site,
        "page": page,
        "pages": (count + LIMIT - 1) // LIMIT,
        "view": 'site'
    })
    return HTMLResponse(content)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
