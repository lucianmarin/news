from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise import fields

class Migration(migrations.Migration):
    initial = True

    operations = [
        ops.CreateModel(
            name='Article',
            fields=[
                ('id', fields.CharField(primary_key=True, unique=True, db_index=True, max_length=32)),
                ('url', fields.TextField(unique=False)),
                ('title', fields.TextField(unique=False)),
                ('domain', fields.CharField(db_index=True, max_length=255)),
                ('site', fields.CharField(db_index=True, max_length=255)),
                ('pub', fields.FloatField()),
                ('author', fields.TextField(null=True, unique=False)),
                ('description', fields.TextField(null=True, unique=False)),
                ('score', fields.FloatField(default=0.0)),
            ],
            options={'table': 'articles', 'app': 'models', 'pk_attr': 'id'},
            bases=['Model'],
        ),
    ]
