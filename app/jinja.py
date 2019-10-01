from jinja2 import Environment, FileSystemBytecodeCache, FileSystemLoader
from app.filters import hostname, shortdate, sitename, superscript

env = Environment()
env.bytecode_cache = FileSystemBytecodeCache()
env.loader = FileSystemLoader('templates/')
# env.auto_reload = True

env.filters['hostname'] = hostname
env.filters['sitename'] = sitename
env.filters['shortdate'] = shortdate
env.filters['superscript'] = superscript

env.globals['brand'] = "NewsFi"
env.globals['v'] = 18
