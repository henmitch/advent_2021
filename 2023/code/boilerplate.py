import os
import re
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

_cookie = os.environ["AOC_SESSION_COOKIE"]
_url = "https://adventofcode.com/2023/day/{}/input"

data_dir = os.path.join(os.path.dirname(__file__), os.pardir, "data")
test_dir = os.path.join(os.path.dirname(__file__), os.pardir, "test")


def file_name(suffix: str = None) -> str:
    caller = os.path.split(sys.argv[0])[1]
    if suffix is not None:
        suffix = "_" + suffix
    else:
        suffix = ""
    return re.sub(r"_[0-9]+\.py", f"{suffix}.txt", caller)


def day_num() -> str:
    return re.match(r"day([0-9]+)", file_name()).group(1).lstrip("0")


def get_data_path(suffix: str = None) -> str:
    out = os.path.join(data_dir, file_name(suffix))
    if os.path.exists(out):
        return out
    url = _url.format(day_num())
    cookies = {
        "session": _cookie,
        "User-agent": "github.com/henmitch/advent at henry@henrymitchell.org"
    }

    data = requests.get(url, cookies=cookies, timeout=10).text
    if data.startswith("Puzzle inputs differ by user.  "
                       "Please log in to get your puzzle input."):
        raise ValueError("Your AoC session cookie is outdated.")
    with open(out, "w") as f:
        f.write(data)
    return out


def get_test_path(suffix: str = None) -> str:
    return os.path.join(test_dir, file_name(suffix))
