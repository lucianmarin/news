from tortoise import fields, models


class Article(models.Model):
    id = fields.CharField(primary_key=True, max_length=32)  # md5 hash
    url = fields.TextField()
    title = fields.TextField()
    domain = fields.CharField(max_length=255, db_index=True)
    site = fields.CharField(max_length=255, db_index=True)
    pub = fields.FloatField()
    author = fields.TextField(null=True)
    description = fields.TextField(null=True)
    score = fields.FloatField(default=0.0)

    class Meta:
        table = "articles"

    def __str__(self):
        return self.id
