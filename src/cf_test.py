import urllib3
import time
from datetime import datetime, timedelta, timezone

from .info.TEST_STATUS import APIStatus

MAA_API = "https://maa.mmirror.top/?test=true"


def get_api(url: str) -> tuple:
    try:

        st = time.perf_counter()
        req = urllib3.request("GET", url, timeout=10, retries=0)
        et = time.perf_counter()

        used = round((et - st) * 1000, 2)

        if req.status == 200:
            return True, req.json(), used
        elif req.status == 403:
            return False, APIStatus.Forbidden, used
        else:
            return False, req.status, used

    except urllib3.exceptions.TimeoutError:
        return False, APIStatus.Timeout
    except urllib3.exceptions.HTTPError:
        return False, APIStatus.HTTPError
    except Exception as e:
        return False, APIStatus.UnknowError, f"Unknow Error: {e}"


def get_time(ts: int | float) -> datetime:
    tz = timezone(timedelta(hours=8))
    ti = datetime.fromtimestamp(int(ts), tz=tz)
    return ti


def run() -> tuple[tuple, datetime]:
    """
    return (status, time)\n
    status: (tuple,datetime)
    """
    status = get_api(MAA_API)
    print(f"CF Workers API: {status}")

    if status[0]:
        return status, get_time(status[1]["time"])
    else:
        return status, datetime.now(timezone(timedelta(hours=8)))
