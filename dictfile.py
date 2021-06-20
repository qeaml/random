from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Any, Dict, Optional, TextIO, Union
from ast import literal_eval


class dictfile:
    @dataclass
    class _cached:
        val: Any
        ttl: datetime

    _cache: Dict[str, _cached]
    _file: TextIO

    def __init__(self, file: Union[TextIO, str]):
        if isinstance(file, str):
            self._file = open(file, "rt")
        else:
            self._file = file

        self._cache = {}

    def get(self, key: str, default=None):
        key = key.lower()
        if key not in self._cache:
            # print("cache miss")
            raw = self._get_from_file(key)
            if raw is None:
                return default
            return literal_eval(raw)
        else:
            # print("cache hit")
            cached = self._cache[key]
            if datetime.now() > cached.ttl:
                # print("  stale")
                del self._cache[key]
                raw = self._get_from_file(key)
                if raw is None:
                    return default
                return literal_eval(raw)
            else:
                # print("  valid")
                cached.ttl = datetime.now() + timedelta(seconds=30)
                return literal_eval(cached.val)

    def __getitem__(self, key: str):
        return self.get(key)

    def _get_from_file(self, key: str) -> Optional[str]:
        self._file.seek(0)
        for line_raw in self._file:
            line = line_raw.strip()

            if line == "" or line.startswith("@"):
                continue

            if line.lower().startswith(key):
                key_raw, *val_elems = line.split(":")
                val_raw = "=".join(val_elems)

                k = key_raw.strip().lower()
                v = val_raw.strip()
                t = datetime.now() + timedelta(seconds=30)

                if k == key:
                    cache_val = self._cached(v, t)
                    self._cache[key] = cache_val
                    return v
        return None


if __name__ == "__main__":
    df = dictfile("dictfile")
    print(df["a"])
    print(df["b"])
    print(df["a"])
