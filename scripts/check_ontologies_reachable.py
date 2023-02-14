import os
import urllib.request
from pathlib import Path
from typing import Union
from urllib.error import HTTPError, URLError

import pandas as pd
import yaml  # type:ignore


def load_yaml(filename: Union[str, Path]):  # pragma: no cover
    with open(filename, "r") as f:
        return yaml.safe_load(f)


VERSIONS_FILE_PATH = Path(f"{os.getcwd()}/bionty/versions/versions.yaml")

versions = load_yaml(VERSIONS_FILE_PATH.resolve())

# We currently assume that the versions.yaml file has the URLs as the final values
flattened_df = pd.json_normalize(versions, sep="_")
flattened_dict = flattened_df.to_dict(orient="records")[0]

failed_urls = []
for url in flattened_dict.values():
    try:
        assert urllib.request.urlopen(url, timeout=100).getcode() == 200
    except (AssertionError, ValueError, HTTPError, URLError) as e:
        failed_urls.append([url, e])

if len(failed_urls) != 0:
    for fail in failed_urls:
        print(fail)
    raise AssertionError(f"{len(failed_urls)} URLs failed.")
