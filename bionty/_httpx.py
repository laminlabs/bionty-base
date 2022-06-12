from typing import Any

import httpx


async def async_get(client, url):
    resp = await client.get(url)
    return resp


def fetch_endpoint(server, request, content_type="application/json", **kwds) -> Any:
    """Fetch an endpoint from the server.

    Allow overriding of default content-type
    """
    r = httpx.get(server + request, headers={"Accept": content_type}, **kwds)

    if content_type == "application/json":
        return r.json()
    else:
        return r.text


def fetch_endpoint_POST(
    server, request, data, content_type="application/json", **kwds
) -> Any:
    """POST requests."""
    r = httpx.post(
        server + request, headers={"Content-Type": content_type}, data=data, **kwds
    )

    if content_type == "application/json":
        return r.json()
    else:
        return r.text
