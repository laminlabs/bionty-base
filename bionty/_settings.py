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
    def dataframe(*args, **kwargs) -> pd.DataFrame:
        # Check if the first argument is self
        idx = 0 if _is_function(args[0]) else 1

        if isinstance(args[idx], pd.DataFrame):
            df = args[idx]
            reformat = False
        else:
            df = pd.DataFrame(index=[d for d in args[idx]])
            reformat = True

        args_new = list(args)
        args_new[idx] = df
        return f(*args_new, _reformat=reformat, **kwargs)

    return dataframe


def _is_function(func) -> bool:
    """Checks if input is a function rather than an instance of class.

    TODO: Is this hacky?
    """
    return hasattr(func, "__name__")


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
