from falcon import API
from app import resources
from project.settings import DEBUG

app = API()

app.req_options.auto_parse_form_urlencoded = True
app.req_options.strip_url_path_trailing_slash = True
app.resp_options.secure_cookies_by_default = False if DEBUG else True

app.add_route('/', resources.MainResource())
app.add_route('/latest', resources.RecentResource())
app.add_route('/about', resources.AboutResource())
app.add_route('/read/{id}', resources.ReadResource())

if DEBUG:
    app.add_route('/static/{filename}', resources.StaticResource())

application = app
