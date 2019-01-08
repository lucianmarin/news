from django.urls import reverse
from jinja2 import Environment, FileSystemBytecodeCache
from app.filters import hostname, sitename, shortdate, superscript


def environment(**options):
    env = Environment(**options)
    env.bytecode_cache = FileSystemBytecodeCache()
    # filters
    env.filters['hostname'] = hostname
    env.filters['sitename'] = sitename
    env.filters['shortdate'] = shortdate
    env.filters['superscript'] = superscript
    # globals
    env.globals['reverse'] = reverse
    env.globals['v'] = 2
    return env
