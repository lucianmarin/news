import time
from django.db import models


class Article(models.Model):
    pub = models.FloatField(default=time.time, db_index=True)
    url = models.URLField(max_length=240, unique=True)
    title = models.CharField(max_length=240, unique=True)
    domain = models.CharField(max_length=120, db_index=True)
    author = models.CharField(max_length=120, default='')
    description = models.TextField(blank=True, null=True)
    has_fb = models.BooleanField(default=False)
    comments = models.IntegerField(default=0, db_index=True)
    reactions = models.IntegerField(default=0, db_index=True)
    shares = models.IntegerField(default=0, db_index=True)
