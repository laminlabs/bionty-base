from pathlib import Path
from typing import Union

import requests  # type:ignore
import yaml  # type:ignore
from rich import print
from rich.progress import Progress


class NoDatesSafeLoader(yaml.SafeLoader):
    @classmethod
    def remove_implicit_resolver(cls, tag_to_remove):
        """Remove implicit resolvers for a particular tag.

        Source: https://stackoverflow.com/questions/34667108/ignore-dates-and-times-while-parsing-yaml

        Takes care not to modify resolvers in super classes.
        """
        if "yaml_implicit_resolvers" not in cls.__dict__:
            cls.yaml_implicit_resolvers = cls.yaml_implicit_resolvers.copy()

        for first_letter, mappings in cls.yaml_implicit_resolvers.items():
            cls.yaml_implicit_resolvers[first_letter] = [
                (tag, regexp) for tag, regexp in mappings if tag != tag_to_remove
            ]


def load_yaml(
    filename: Union[str, Path], convert_dates: bool = True
):  # pragma: no cover
    if not convert_dates:
        NoDatesSafeLoader.remove_implicit_resolver("tag:yaml.org,2002:timestamp")

        with open(filename, "r") as f:
            return yaml.load(f, Loader=NoDatesSafeLoader)

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
