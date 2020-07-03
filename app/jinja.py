from jinja2 import Environment, FileSystemBytecodeCache, FileSystemLoader
from app.filters import hostname, shortdate, sitename, superscript, truncate
from project.settings import DEBUG

env = Environment()
env.bytecode_cache = FileSystemBytecodeCache()
env.loader = FileSystemLoader('templates/')
env.auto_reload = DEBUG

env.filters['hostname'] = hostname
env.filters['sitename'] = sitename
env.filters['shortdate'] = shortdate
env.filters['superscript'] = superscript
env.filters['truncate'] = truncate

env.globals['brand'] = "Artificial Feed"
env.globals['v'] = 4
