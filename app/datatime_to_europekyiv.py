import datetime
import pytz


def get_kyiv_timezone(creation_date: datetime.datetime, europekyiv: str, fmt: str) -> str:
    return creation_date.replace(tzinfo=pytz.utc).astimezone(tz=pytz.timezone(europekyiv)).strftime(fmt)
