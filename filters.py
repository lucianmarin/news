import datetime
import urllib


def hostname(value):
    """Get hostname from an url."""
    url = urllib.parse.urlsplit(value)
    return url.netloc.replace('www.', '')


def date(struct):
    timestamp = datetime.datetime.fromtimestamp(struct)
    return timestamp.strftime('%b %-e, %Y %H:%M')


def shortdate(struct):
    """Short time interval for a timestamp."""
    timestamp = datetime.datetime.utcfromtimestamp(struct)
    delta = datetime.datetime.utcnow() - timestamp

    miliseconds = abs(delta.microseconds) // 1000
    seconds = abs(delta.seconds)
    days = abs(delta.days) % 365
    years = abs(delta.days) // 365
    weeks = days // 7

    if not years and not days:
        if not seconds:
            return "%dms" % miliseconds
        elif seconds < 60:
            return "%ds" % seconds
        elif seconds < 3600:
            return "%dm" % (seconds // 60)
        else:
            return "%dh" % (seconds // 3600)
    elif not years:
        if not weeks:
            return "%dd" % days
        else:
            return "%dw" % weeks
    else:
        if not weeks and not days:
            return "%dy" % years
        elif not weeks:
            return "%dy, %dd" % (years, days)
        else:
            return "%dy, %dw" % (years, weeks)
