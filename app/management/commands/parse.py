import gzip
from datetime import datetime, timedelta
from collections import defaultdict

from dateutil.parser import parse
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Fetch articles from feeds."

    @property
    def days_back(self):
        strings = []
        for day in range(0, 3):
            d_str = (datetime.now() - timedelta(day)).strftime('%d/%b/%Y')
            strings.append(d_str)
        return strings

    def grab_ips(self):
        days = defaultdict(set)
        with gzip.open("newscafe.log.gz", "rt") as f:
            for line in f:
                cols = line.split()
                ip = cols[0]
                line_day = cols[3][1:].split(':', 1)[0]
                if 'bot' not in line.lower():
                    days[line_day].add(ip)
        return days

    def handle(self, *args, **options):
        ips = self.grab_ips()
        for key, item in ips.items():
            print(parse(key).strftime('%Y-%m-%d'), len(item))
        # print(ips, 'readers')
