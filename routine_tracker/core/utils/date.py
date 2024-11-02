from datetime import datetime, timedelta
from typing import Any, Optional, Union
from urllib.parse import parse_qs

from django.http import HttpRequest
from django.utils.timezone import make_aware


class daterange:
    def __init__(self, start: Union[str, datetime], end: Optional[Union[str, datetime]] = None):
        self.start = self._parse_date(start)
        self.end = self._parse_date(end or datetime.now())
        self._alter_dates()

    def _parse_date(self, date: Union[str, datetime]) -> datetime:
        if isinstance(date, str):
            return datetime.strptime(date, "%Y-%m-%d")
        return date

    def _alter_dates(self):
        """Alter the start and end dates to include the entire day."""

        self.start = self.start.replace(hour=0, minute=0, second=0)
        self.end = self.end.replace(hour=23, minute=59, second=59)

    def __iter__(self):
        current = self.start
        while current <= self.end:
            yield make_aware(current).date()
            current += timedelta(days=1)

    def __contains__(self, item: Any) -> bool:
        if not isinstance(item, datetime):
            return False

        return self.start <= item <= self.end

    def __len__(self) -> int:
        difference = (self.end - self.start).days + 1

        if difference < 0:
            return 0

        return difference


def get_default_daterange() -> daterange:
    return daterange(datetime.now() - timedelta(days=7))


def get_daterange(request: HttpRequest) -> daterange:
    if request.htmx:
        if request.headers.get("HX-Navigation") == "true":
            return get_default_daterange()

        query_params = parse_qs(request.headers.get("HX-Current-Url", "").split("?")[-1])
        start = query_params.get("from", [None])[0]
        end = query_params.get("to", [None])[0]
    else:
        start = request.GET.get("from")
        end = request.GET.get("to")

    if not start:
        return get_default_daterange()

    try:
        return daterange(start, end)
    except ValueError:
        return get_default_daterange()
