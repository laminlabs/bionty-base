from pathlib import Path
from typing import Union

import requests  # type:ignore
import yaml  # type:ignore
from rich import print
from rich.progress import Progress


def load_yaml(filename: Union[str, Path]):  # pragma: no cover
    with open(filename, "r") as f:
        return yaml.safe_load(f)


def write_yaml(data: dict, filename: Union[str, Path]):  # pragma: no cover
    with open(filename, "w") as f:
        yaml.dump(data, f)


def url_download(  # pragma: no cover
    url: str, filename: Union[str, Path, None] = None, block_size: int = 1024, **kwargs
) -> None:
    """Downloads a file to a specified path.

    Args:
        url: The URL to download.
        filename: The path to download the file to.
        block_size: Buffer size in bytes for sending a file-like message body.
        **kwargs: Keyword arguments are passed to 'requests'

    Raises:
        HttpError: If the request response is not 200 and OK.
    """
    try:
        response = requests.get(url, stream=True, allow_redirects=True, **kwargs)
        response.raise_for_status()

        total_content_length = int(response.headers.get("content-length", 0))
        if filename is None:
            filename = url.split("/")[-1]

        with Progress(refresh_per_second=10000) as progress:
            task = progress.add_task("[red]Downloading...", total=total_content_length)

            with open(filename, "wb") as file:
                for data in response.iter_content(block_size):
                    file.write(data)
                    progress.update(task, advance=block_size)

    except requests.exceptions.HTTPError as err:
        print(err)
