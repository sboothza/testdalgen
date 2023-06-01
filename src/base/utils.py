from pathlib import Path
from typing import List


def split_clean(value: str, sep: str) -> List[str]:
    return list(filter(None, value.split(sep)))


def get_fullname(path: str) -> str:
    p = Path(path)
    p.resolve()
    return str(p.expanduser())


def get_filename(path: str) -> str:
    p = Path(path)
    p.resolve()
    return str(p.expanduser()).replace(str(p.parent), "").replace("/", "")
