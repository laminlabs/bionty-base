import sys
from typing import Any

import requests  # type: ignore


def fetch_endpoint(server, request, content_type) -> Any:
    """Fetch an endpoint from the server.

    Allow overriding of default content-type
    """
    r = requests.get(server + request, headers={"Accept": content_type})

    if not r.ok:
        r.raise_for_status()
        sys.exit()

    if content_type == "application/json":
        return r.json()
    else:
        return r.text


def fetch_endpoint_POST(server, request, data, content_type="application/json") -> Any:
    """POST requests."""
    r = requests.post(
        server + request, headers={"Content-Type": content_type}, data=data
    )

    if not r.ok:
        r.raise_for_status()
        sys.exit()

    if content_type == "application/json":
        return r.json()
    else:
        return r.text
