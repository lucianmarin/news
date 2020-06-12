import time
from os import environ

from django import setup
from django.conf import settings
from django.db import models

if not settings.configured:
    environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    setup()

if settings.DEBUG:
    import logging
    log = logging.getLogger('django.db.backends')
    log.setLevel(logging.DEBUG)
    log.addHandler(logging.StreamHandler())


class Article(models.Model):
    pub = models.FloatField(default=time.time, db_index=True)
    url = models.URLField(max_length=240, unique=True)
    title = models.CharField(max_length=240, unique=True)
    domain = models.CharField(max_length=120, db_index=True)
    author = models.CharField(max_length=120, default='')
    description = models.TextField(blank=True, null=True)
    has_fb = models.BooleanField(default=False)
    comments = models.IntegerField(default=0)
    reactions = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    score = models.IntegerField(default=0, db_index=True)

    @property
    def base(self):
        number = self.id
        alphabet, base36 = "0123456789abcdefghijklmnopqrstuvwxyz", ""
        while number:
            number, i = divmod(number, 36)
            base36 = alphabet[i] + base36
        return base36 or alphabet[0]

    @property
    def icon(self):
        if self.domain in ['axios.com', 'qz.com', 'vox.com']:
            return "/icons/{0}.jpg".format(self.domain)
        else:
            return "/static/192.png"

    @property
    def reach(self):
        reach = str(round(self.score / 3, 1))
        first, last = reach.split('.')
        reach = first if last == '0' else reach
        return reach
