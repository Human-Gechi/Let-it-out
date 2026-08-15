import asyncio
import time
from collections.abc import Callable

from fastapi import HTTPException, Request, status
from backend.app.config import get_settings

_buckets: dict[str, dict] = {}
_lock = asyncio.Lock()

settings = get_settings()
def rate_limit_dependency(
    times: int = 10,
    seconds: int = 60,
    key_fn: Callable[[Request], str] = lambda req: req.client.host,
):
    capacity = float(times)
    refill_per_sec = times / seconds

    async def _dep(request: Request):
        key = key_fn(request) or "anon"
        now = time.monotonic()

        async with _lock:
            bucket = _buckets.get(key)
            if bucket is None:
                _buckets[key] = {"tokens": capacity - 1.0, "last": now}
                return

            elapsed = now - bucket["last"]
            bucket["tokens"] = min(
                capacity, bucket["tokens"] + elapsed * refill_per_sec
            )
            bucket["last"] = now

            if bucket["tokens"] >= 1.0:
                bucket["tokens"] -= 1.0
                return

            missing = 1.0 - bucket["tokens"]
            retry_after = int((missing / refill_per_sec) + 1)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests",
                headers={"Retry-After": str(retry_after)},
            )

    return _dep
