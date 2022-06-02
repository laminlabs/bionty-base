from functools import wraps
from pathlib import Path
from typing import Iterable, Union

import pandas as pd


def check_datasetdir_exists(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        settings.datasetdir.mkdir(exist_ok=True)
        return f(*args, **kwargs)

    return wrapper


def format_into_dataframe(f):
    @wraps(f)
    def format(data: Iterable, *args, **kwargs):
        result = f(data=data, *args, **kwargs)
        if not isinstance(result, pd.DataFrame):
            df = pd.DataFrame(index=[d for d in data])
        else:
            df = data
        return df

    return format


class Settings:
    def __init__(self, datasetdir: Union[str, Path] = Path("./data/")):
        self._datasetdir = datasetdir

    @property
    def datasetdir(self):
        """Directory for datasets."""
        return self._datasetdir

    @datasetdir.setter
    def datasetdir(self, datasetdir: Union[str, Path]):
        self._datasetdir = Path(datasetdir).resolve()


settings = Settings()
