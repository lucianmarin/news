from os import environ
import time
from django import setup
from django.conf import settings
from django.db import models

if not settings.configured:
    environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    setup()


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
