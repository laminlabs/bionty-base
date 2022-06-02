from functools import wraps
from pathlib import Path
from typing import Union

import pandas as pd


def check_datasetdir_exists(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        settings.datasetdir.mkdir(exist_ok=True)
        return f(*args, **kwargs)

    return wrapper


def format_into_dataframe(f):
    @wraps(f)
    def dataframe(self, data, *args, **kwargs) -> pd.DataFrame:
        df = (
            data
            if isinstance(data, pd.DataFrame)
            else pd.DataFrame(index=[d for d in data])
        )
        return f(self, df, *args, **kwargs)

    return dataframe


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
