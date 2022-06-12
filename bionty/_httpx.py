import asyncio
import sys
from typing import Any

import httpx
import nest_asyncio
import requests  # type: ignore
from syncer import sync

nest_asyncio.apply()  # Fixes the issue with iPython compatibility


async def _async_get(client, url, content_type="application/json"):
    resp = await client.get(url, headers={"content-type": content_type})

    if resp.headers["content-type"].find("application/json") > -1:
        return resp.json()
    else:
        return resp.text


@sync
async def get_request_async(
    server_request: str, terms, content_type="application/json"
):
    async with httpx.AsyncClient() as client:

        tasks = []

        for term in terms:
            url = f"{server_request}{term}"
            tasks.append(
                asyncio.ensure_future(
                    _async_get(client, url, content_type=content_type)
                )
            )

        resps = await asyncio.gather(*tasks)

    return resps


def get_request(server, request, content_type="application/json", **kwds) -> Any:
    """Fetch an endpoint from the server.

    Allow overriding of default content-type
    """
    r = requests.get(server + request, headers={"Accept": content_type}, **kwds)

    if not r.ok:
        r.raise_for_status()
        sys.exit()

    if content_type == "application/json":
        return r.json()
    else:
        return r.text


def post_request(server, request, data, content_type="application/json", **kwds) -> Any:
    """POST requests."""
    r = requests.post(
        server + request, headers={"Content-Type": content_type}, data=data, **kwds
    )

    if not r.ok:
        r.raise_for_status()
        sys.exit()

    if content_type == "application/json":
        return r.json()
    else:
        return r.text
