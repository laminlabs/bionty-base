from functools import wraps
from pathlib import Path
from typing import Union

import boto3
from cloudpathlib import S3Client

ROOT_DIR = Path(__file__).parent.resolve()


def s3_bionty_assets(filename: str):
    client = S3Client(
        local_cache_dir=settings.datasetdir,
        no_sign_request=True,
        boto3_session=boto3.Session(),
    )
    return client.CloudPath(f"s3://bionty-assets/{filename}")


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
