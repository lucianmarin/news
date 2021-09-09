from falcon import App
from falcon.constants import MEDIA_HTML

from app import resources
from project.settings import DEBUG

app = App(media_type=MEDIA_HTML)

app.req_options.auto_parse_form_urlencoded = True
app.req_options.strip_url_path_trailing_slash = True

app.resp_options.secure_cookies_by_default = not DEBUG

app.add_route('/', resources.MainResource())
app.add_route('/link/{base}', resources.LinkResource())
app.add_route('/read/{base}', resources.ReadResource())


if DEBUG:
    app.add_route('/static/{filename}', resources.StaticResource())

application = app
