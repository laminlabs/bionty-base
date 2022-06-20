import pickle
from pathlib import Path
from typing import Union

from typeguard import typechecked


@typechecked
def read_pickle(filename: Union[str, Path]) -> dict:
    with open(filename, "rb") as handle:
        return pickle.load(handle)


@typechecked
def write_pickle(data: dict, filename: Union[str, Path]) -> None:
    with open(filename, "wb") as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
