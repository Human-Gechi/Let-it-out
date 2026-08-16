import asyncio
from collections.abc import Callable
from typing import Any

import httpx
import pytest

from backend.app.main import app


@pytest.fixture
def api_request() -> Callable[..., httpx.Response]:
    def request(method: str, path: str, **kwargs: Any) -> httpx.Response:
        async def send() -> httpx.Response:
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(
                transport=transport,
                base_url="http://testserver",
            ) as client:
                return await client.request(method, path, **kwargs)

        return asyncio.run(send())

    return request
