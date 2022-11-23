from pathlib import Path
from typing import Union

import requests  # type:ignore
import yaml  # type:ignore


def load_yaml(filename: Union[str, Path]):
    with open(filename, "r") as f:
        return yaml.safe_load(f)


def write_yaml(data: dict, filename: Union[str, Path]):
    with open(filename, "w") as f:
        yaml.dump(data, f)


def url_download(url: str, filename: Union[str, Path, None] = None, **kwargs):
    r = requests.get(url, allow_redirects=True, **kwargs)
    if r.status_code != 200:
        raise ConnectionError(f"could not download {url}\nerror code: {r.status_code}")

    if filename is None:
        filename = url.split("/")[-1]

    Path(filename).write_bytes(r.content)
