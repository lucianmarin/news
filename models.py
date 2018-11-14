import rom
import time


class News(rom.Model):
    time = rom.Float(default=time.time, index=True)
    link = rom.Text(required=True, unique=True, prefix=True, keygen=rom.SIMPLE)
    title = rom.Text(required=True)
    author = rom.Text()
    description = rom.Text()
    shares = rom.Integer(index=True)
    comments = rom.Integer(index=True)
