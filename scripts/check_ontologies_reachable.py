import os
import urllib.request
from pathlib import Path
from urllib.error import HTTPError, URLError

import pandas as pd

from bionty.dev._io import load_yaml

VERSIONS_FILE_PATH = Path(f"{os.getcwd()}/../bionty/versions/versions.yaml")

versions = load_yaml(VERSIONS_FILE_PATH.resolve())

# We currently assume that the versions.yaml file has the structure:
# Name -> database -> versions -> actual version with value URL
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
