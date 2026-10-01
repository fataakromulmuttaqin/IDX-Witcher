import functools
import json

import redis

from core.config import get_settings

_r = redis.Redis.from_url(get_settings().redis_url, decode_responses=True)
PREFIX = "iw:"


def cached(ttl: int = 6 * 3600):
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(**kwargs):
            key = f"{PREFIX}{fn.__name__}:{json.dumps(kwargs, sort_keys=True, default=str)}"
            try:
                hit = _r.get(key)
                if hit:
                    return json.loads(hit)
            except redis.RedisError:
                pass
            out = fn(**kwargs)
            try:
                _r.setex(key, ttl, json.dumps(out, default=str))
            except redis.RedisError:
                pass
            return out

        return wrapper

    return deco


def purge() -> None:
    try:
        for k in _r.scan_iter(f"{PREFIX}*"):
            _r.delete(k)
    except redis.RedisError:
        pass
