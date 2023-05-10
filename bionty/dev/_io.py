from pathlib import Path
from typing import Union

import requests  # type:ignore
import yaml  # type:ignore
from rich import print
from rich.progress import Progress

from bionty._settings import settings
from bionty.dev._upath import UPath


def load_yaml(
    filename: Union[str, Path], convert_dates: bool = True
):  # pragma: no cover
    with open(filename, "r") as f:
        return yaml.safe_load(f)


def write_yaml(
    data: dict,
    filename: Union[str, Path],
    sort_keys: bool = False,
    default_flow_style: bool = False,
):  # pragma: no cover
    with open(filename, "w") as f:
        yaml.dump(
            data,
            f,
            sort_keys=sort_keys,
            default_flow_style=default_flow_style,
        )


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


def s3_bionty_assets(
    filename: str, localpath: Path = None, assets_base_url: str = "s3://bionty-assets"
):
    """Synchronizes a S3 file path with local file storage.

    If the file does not exist locally it gets downloaded.
    If the file does not exist on S3, the file does not get synchronized.

    Args:
        filename: The suffix of the assets_base_url.
        localpath: The Path to the local file.
        assets_base_url: The S3 base URL. Prefix of the filename.

    Returns:
        A Path object of the synchronized path.
    """
    cloudpath = UPath(f"{assets_base_url}/{filename}", anon=True, cache_regions=True)
    if not localpath:
        localpath = settings.datasetdir / filename

    cloudpath.bt_synchronize(localpath)

    return localpath
