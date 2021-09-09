import time
from os import environ

from django import setup
from django.conf import settings
from django.db import models
from django.contrib.postgres import fields


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
    paragraphs = fields.ArrayField(models.TextField(), default=list)
    ips = fields.ArrayField(models.TextField(), default=list)

    @property
    def base(self):
        number = self.pk
        alphabet, base36 = "0123456789abcdefghijklmnopqrstuvwxyz", ""
        while number:
            number, i = divmod(number, 36)
            base36 = alphabet[i] + base36
        return base36 or alphabet[0]

    @property
    def reach(self):
        rounded = round(self.score / 3000)
        if rounded:
            return "{0}k".format(rounded)
        else:
            return self.score

    def increment(self, ip):
        self.ips += [ip]
        self.ips = list(set(self.ips))
        self.score = len(self.ips)
        self.save(update_fields=['ips', 'score'])
