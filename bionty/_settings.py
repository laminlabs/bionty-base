from functools import wraps
from pathlib import Path
from typing import Union

from lndb.dev.upath import UPath

HOME_DIR = Path(f"{Path.home()}/.lamin/bionty").resolve()
ROOT_DIR = Path(__file__).parent.resolve()


def s3_bionty_assets(
    filename: str, localpath: Path = None, assets_base_url: str = "s3://bionty-assets"
):
    cloudpath = UPath(f"{assets_base_url}/{filename}", anon=True, cache_regions=True)
    if not localpath:
        localpath = settings.datasetdir / filename

    cloudpath.synchronize(localpath)

    return localpath


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


class Settings:
    def __init__(
        self,
        datasetdir: Union[str, Path] = ROOT_DIR / "data/",
        dynamicdir: Union[str, Path] = ROOT_DIR / "_dynamic/",
        versionsdir: Union[str, Path] = HOME_DIR / "versions/",
    ):
        # setters convert to Path and resolve:
        self.datasetdir = datasetdir
        self.dynamicdir = dynamicdir
        self.versionsdir = versionsdir

        self.versionsdir.mkdir(exist_ok=True, parents=True)  # type: ignore

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

    @property
    def versionsdir(self):
        """Directory for version yamls."""
        return self._versionsdir

    @versionsdir.setter
    def versionsdir(self, versionsdir: Union[str, Path]):
        self._versionsdir = Path(versionsdir).resolve()


settings = Settings()
