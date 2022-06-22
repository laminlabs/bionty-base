from functools import wraps
from pathlib import Path
from typing import Union

import pandas as pd

ROOT_DIR = Path(__file__).parent.resolve()


def check_datasetdir_exists(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        settings.datasetdir.mkdir(exist_ok=True)
        return f(*args, **kwargs)

    return wrapper


def check_dynamicdir_exists(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        settings.dynamicdir.mkdir(exist_ok=True)
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


@check_dynamicdir_exists
def dump_dataclass_as_private_module(obj):
    """Save the dataclass as python code."""
    header = f"from pydantic import BaseModel\n\n\nclass {obj.__name__}(BaseModel):\n"
    with open(settings.dynamicdir / f"{obj.__name__.lower()}.py", "w") as f:
        f.write(header)
        for key, value in obj().__fields__.items():
            f.write(f"    {key} : {value.type_.__name__} = {value.default!r}\n")


class Settings:
    def __init__(
        self,
        datasetdir: Union[str, Path] = ROOT_DIR / "data/",
        dynamicdir: Union[str, Path] = ROOT_DIR / "_dynamic/",
    ):
        self.datasetdir = datasetdir
        self.dynamicdir = dynamicdir

    @property
    def datasetdir(self):
        """Directory for datasets."""
        return self._datasetdir

    @datasetdir.setter
    def datasetdir(self, datasetdir: Union[str, Path]):
        self._datasetdir = Path(datasetdir).resolve()

    @property
    def dynamicdir(self):
        """Directory for datasets."""
        return self._dynamicdir

    @dynamicdir.setter
    def dynamicdir(self, dynamicdir: Union[str, Path]):
        self._dynamicdir = Path(dynamicdir).resolve()


settings = Settings()
