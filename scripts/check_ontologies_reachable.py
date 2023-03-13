import os
import urllib.request
from pathlib import Path
from typing import Dict, List
from urllib.error import HTTPError, URLError

import yaml  # type:ignore

VERSIONS_FILE_PATH = Path(f"{os.getcwd()}/bionty/versions/versions.yaml")


def get_yaml_key_values(
    yaml_file_path: Path, key: str = "versions"
) -> List[Dict[str, str]]:
    """Extracts the version pairs from the versions file.

    Args:
        yaml_file_path: Path to the yaml file.
        key: The key of all versions

    Returns:
        A list of Dictionaries of versions to URLs.
    """
    with open(yaml_file_path, "r") as stream:
        versions = yaml.safe_load(stream)
    key_values = []

    for k, v in versions.items():
        if k == key:
            key_values.append(v)
        elif isinstance(v, dict):

            def get_key_values_from_dict(dictionary: Dict, key: str):
                key_values = []
                for k, v in dictionary.items():
                    if k == key:
                        key_values.append(v)
                    elif isinstance(v, dict):
                        nested_key_values = get_key_values_from_dict(v, key)
                        key_values.extend(nested_key_values)
                return key_values

            nested_key_values = get_key_values_from_dict(v, key)
            key_values.extend(nested_key_values)

    return key_values


versions_only = get_yaml_key_values(VERSIONS_FILE_PATH.resolve(), key="versions")

failed_urls = []
for pair in versions_only:
    for url_md5s in pair.values():
        url = url_md5s[0]
        if url.startswith("http"):
            try:
                assert urllib.request.urlopen(url, timeout=1000).getcode() == 200
            except URLError:
                print(f"URL: {url} is currently not accessible.")
                pass
            except (AssertionError, ValueError, HTTPError) as e:
                failed_urls.append([url, e])

if len(failed_urls) != 0:
    for fail in failed_urls:
        print(fail)
    raise AssertionError(f"{len(failed_urls)} URLs failed.")
