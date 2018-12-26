from datetime import datetime
import urllib


def hostname(value):
    """Get hostname from an url."""
    url = urllib.parse.urlsplit(value)
    return url.netloc.replace('www.', '')


def date(stamp):
    """Format date time."""
    timestamp = datetime.fromtimestamp(stamp)
    return timestamp.strftime('%b %-e, %Y %H:%M')


def shortdate(stamp):
    """Short time interval for a timestamp."""
    timestamp = datetime.utcfromtimestamp(stamp)
    delta = datetime.utcnow() - timestamp
    miliseconds = int(delta.microseconds) // 1000
    seconds = int(delta.total_seconds())
    minutes = seconds // 60
    hours = seconds // 3600
    if not hours and not minutes and not seconds:
        return f"{miliseconds}ms"
    if not hours and not minutes:
        return f"{seconds}s"
    if not hours:
        return f"{minutes}m"
    return f"{hours}h"
