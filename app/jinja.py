from jinja2 import Environment, FileSystemBytecodeCache, FileSystemLoader
from app.filters import hostname, sitename, shortdate, superscript


env = Environment()
env.loader = FileSystemLoader('templates/')
env.bytecode_cache = FileSystemBytecodeCache()

# filters
env.filters['hostname'] = hostname
env.filters['sitename'] = sitename
env.filters['shortdate'] = shortdate
env.filters['superscript'] = superscript

# globals
env.globals['brand'] = "NewsFi"
env.globals['v'] = 18
