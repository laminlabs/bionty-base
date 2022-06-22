import pickle
from pathlib import Path
from typing import Union

import orjson
from typeguard import typechecked


@typechecked
def read_pickle(filename: Union[str, Path]):
    with open(filename, "rb") as handle:
        return pickle.load(handle)


def loads_pickle(filename: Union[str, Path]):
    with open(filename, "rb") as handle:
        r = pickle.load(handle)
    return pickle.loads(r)


@typechecked
def write_pickle(data, filename: Union[str, Path]) -> None:
    with open(filename, "wb") as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)


@typechecked
def read_json(filename: Union[str, Path]):
    with open(filename, "rb") as f:
        return orjson.loads(f.read())


@typechecked
def write_json(data, filename: Union[str, Path]):
    with open(filename, "wb") as f:
        f.write(orjson.dumps(data))
