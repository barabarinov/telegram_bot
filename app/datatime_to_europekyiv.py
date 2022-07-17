import pytz


def get_kyiv_timezone(creation_date, europekiev, fmt):
    return creation_date.replace(tzinfo=pytz.utc).astimezone(tz=pytz.timezone(europekiev)).strftime(fmt)
