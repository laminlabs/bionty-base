"""Original implementation: https://github.com/laminlabs/lndb/blob/157c8e90d07241b8b2a43abcc420a0f9b690ade5/lndb/dev/upath.py#L46."""

import os
from datetime import timezone
from pathlib import Path
from typing import Union

import fsspec
from dateutil.parser import isoparse  # type: ignore
from lamin_logger import logger
from upath import UPath


def infer_filesystem(path: Union[Path, UPath, str]):
    path_str = str(path)

    if isinstance(path, UPath):
        fs = path.fs
    else:
        protocol = fsspec.utils.get_protocol(path_str)
        if protocol == "s3":
            fs_kwargs = {"cache_regions": True}
        else:
            fs_kwargs = {}
        fs = fsspec.filesystem(protocol, **fs_kwargs)

    return fs, path_str


def _download_to(self, path, **kwargs):
    self.fs.download(str(self), str(path), **kwargs)


def _upload_from(self, path, **kwargs):
    self.fs.upload(str(path), str(self), **kwargs)


def _synchronize(self, filepath: Path):
    if not self.exists():
        return None

    if not filepath.exists():
        filepath.parent.mkdir(parents=True, exist_ok=True)
        mts = self.bt_modified.timestamp()
        self.bt_download_to(filepath)
        os.utime(filepath, times=(mts, mts))
        return None

    cloud_mts = self.bt_modified.timestamp()
    local_mts = filepath.stat().st_mtime
    if cloud_mts > local_mts:
        mts = self.bt_modified.timestamp()
        self.bt_download_to(filepath)
        os.utime(filepath, times=(mts, mts))
    elif cloud_mts < local_mts:
        logger.warning(
            f"Local file ({filepath}) for cloud path ({self}) is newer on disk than in cloud.\n"  # noqa
            "It seems you manually updated the database locally and didn't push changes to the cloud.\n"  # noqa
            "This can lead to data loss if somebody else modified the cloud file in"  # noqa
            " the meantime."
        )


def _modified(self):
    path = str(self)
    if "gcs" not in self.fs.protocol:
        mtime = self.fs.modified(path)
    else:
        stat = self.fs.stat(path)
        if "updated" in stat:
            mtime = stat["updated"]
            mtime = isoparse(mtime)
        else:
            return None
    # always convert to the local timezone before returning
    # assume in utc if the time zone is not specified
    if mtime.tzinfo is None:
        mtime = mtime.replace(tzinfo=timezone.utc)
    return mtime.astimezone().replace(tzinfo=None)


UPath.bt_download_to = _download_to
UPath.bt_upload_from = _upload_from
UPath.bt_synchronize = _synchronize
UPath.bt_modified = property(_modified)
