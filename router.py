from falcon import App
from falcon.constants import MEDIA_HTML

from app import resources
from app.settings import DEBUG

app = App(media_type=MEDIA_HTML)

app.req_options.strip_url_path_trailing_slash = True
app.resp_options.secure_cookies_by_default = not DEBUG

app.add_route('/', resources.BreakingResource())
app.add_route('/current', resources.CurrentResource())
app.add_route('/read/{base}', resources.ReadResource())
app.add_route('/about', resources.AboutResource())

if DEBUG:
    app.add_route('/static/{filename}', resources.StaticResource())

application = app
