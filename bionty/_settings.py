from functools import wraps
from pathlib import Path
from typing import Union


def check_datasetdir_exists(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        settings.datasetdir.mkdir(exist_ok=True)
        return f(*args, **kwargs)

    return wrapper


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
