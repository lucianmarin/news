from datetime import datetime
import urllib


def hostname(value):
    """Get hostname from an url."""
    url = urllib.parse.urlsplit(value)
    return url.netloc.replace('www.', '')


def date(struct):
    """Format date time."""
    timestamp = datetime.fromtimestamp(struct)
    return timestamp.strftime('%b %-e, %Y %H:%M')


def shortdate(struct):
    """Short time interval for a timestamp."""
    timestamp = datetime.utcfromtimestamp(struct)
    delta = datetime.utcnow() - timestamp

    miliseconds = abs(delta.microseconds) // 1000
    seconds = abs(delta.seconds)
    minutes = seconds // 60
    hours = seconds // 3600

    if not hours and not minutes and not seconds:
        return "%dms" % miliseconds
    elif not hours and not minutes:
        return "%ds" % seconds
    elif not hours:
        return "%dm" % minutes
    else:
        return "%dh" % hours
