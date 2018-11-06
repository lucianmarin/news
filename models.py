import json
import rom
import time


class News(rom.Model):
    time = rom.Float(default=time.time, index=True)
    link = rom.Text(required=True, unique=True, prefix=True, keygen=rom.SIMPLE)
    title = rom.Text(required=True)
    author = rom.Text()
    description = rom.Text()
    shares = rom.Integer(index=True)


# with open('remote-db.json', 'r') as db_file:
#     DB = json.loads(db_file.read())

# News.query.delete()

# for value in DB.values():
#     n = News(link=value['link'], title=value['title'])
#     n.time = value.get('time', 0)
#     n.author = value.get('author', '')
#     n.description = value.get('description', '')
#     n.shares = value.get('shares', 0)
#     n.save()

# print(News.query.count())
