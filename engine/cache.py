# engine/cache.py

"""
Taylor NQ Cache

Simple in-memory cache used throughout the application to avoid
unnecessary downloads and recalculations.

No UI.
No calculations.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any


@dataclass(slots=True)
class CacheItem:

    value: Any

    expires: datetime


class Cache:

    def __init__(self):

        self._cache: dict[str, CacheItem] = {}

    def get(self, key: str):

        item = self._cache.get(key)

        if item is None:
            return None

        if datetime.now() >= item.expires:

            del self._cache[key]

            return None

        return item.value

    def set(
        self,
        key: str,
        value: Any,
        ttl_seconds: int,
    ):

        self._cache[key] = CacheItem(
            value=value,
            expires=datetime.now() + timedelta(seconds=ttl_seconds),
        )

    def delete(self, key: str):

        if key in self._cache:
            del self._cache[key]

    def clear(self):

        self._cache.clear()

    def contains(self, key: str) -> bool:

        return self.get(key) is not None

    def keys(self):

        return list(self._cache.keys())

    def size(self):

        return len(self._cache)


cache = Cache()
