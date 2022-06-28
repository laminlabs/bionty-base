from pathlib import Path
from typing import Union

import orjson
from typeguard import typechecked


@typechecked
def read_json(filename: Union[str, Path]):
    with open(filename, "rb") as f:
        return orjson.loads(f.read())
