import rom
import time


class News(rom.Model):
    time = rom.Float(default=time.time, index=True)
    link = rom.Text(required=True, unique=True)
    title = rom.Text(required=True, unique=True)
    site = rom.Text(index=True, keygen=rom.IDENTITY_CI)
    author = rom.Text()
    description = rom.Text()
    shares = rom.Integer(index=True)
