import shutil
from pathlib import Path
from typing import Any, Dict, Literal

import pandas as pd

from bionty._settings import settings
from bionty.dev._io import load_yaml, write_yaml

ROOT = Path(__file__).parent.parent / "versions"
VERSIONS_PATH = ROOT / "versions.yaml"
_CURRENT_PATH = ROOT / "._current.yaml"
_LNDB_PATH = ROOT / "._lndb.yaml"

_LOCAL_PATH = settings.versionsdir / "local.yaml"


def latest_db_version(db: str) -> str:
    """Lookup the latest version of a database.

    Args:
        db: The database to look up the version for.

    Returns:
        The version of the database. Usually a date.
    """
    db = db.lower()

    if db == "ensembl":
        # For Ensembl, parse the current_README file
        lines = []

        for line in pd.read_csv(
            "https://ftp.ensembl.org/pub/README",
            chunksize=1,
            header=None,
            encoding="utf-8",
        ):
            lines.append(line.iloc[0, 0])
        return "-".join(lines[1].split(" ")[1:-1]).lower()

    else:
        raise NotImplementedError


def create_current(
    overwrite: bool = True, source: Literal["versions", "local"] = "local"
) -> None:
    """Writes the most recent version to the _current.yaml .

    Takes the 1st database defined in the source.

    Args:
        overwrite: Whether to overwrite the _current.yaml even if it exists already.
        source: The yaml source to use to create the _current.yaml . Defaults to local.
    """
    if not _CURRENT_PATH.exists() or overwrite:
        versions = (
            load_yaml(VERSIONS_PATH) if source == "versions" else load_yaml(_LOCAL_PATH)
        )

        def _write_current_yaml(versions):
            _current = {}
            for name, db_versions in versions.items():
                # this will only take the 1st db if multiple exists for the same entity
                db = next(iter(db_versions))
                versions = db_versions.get(db).get("versions")
                version = str(sorted(versions.keys(), reverse=True)[0])
                _current[name] = {db: version}
            return _current

        _current = _write_current_yaml(versions)
        write_yaml(_current, _CURRENT_PATH)


def create_local(overwrite: bool = True) -> None:
    """If _local.yaml doesn't exist, copy from versions.yaml and create it.

    Args:
        overwrite: Whether to overwrite the current _local.yaml .
    """
    if not _LOCAL_PATH.exists() or overwrite:
        versions = load_yaml(VERSIONS_PATH)

        write_yaml(versions, _LOCAL_PATH)


def update_local(to_update_yaml: Dict[Any, Any]) -> None:
    """Update _local to add additional entries from the public versions.yaml table.

    Args:
        to_update_yaml: Dictionary of the current _local.yaml .
    """
    versions = load_yaml(VERSIONS_PATH)

    for entity, dbs in versions.items():
        if entity not in to_update_yaml:
            to_update_yaml[entity] = versions[entity]
        else:
            for db_name, v in dbs.items():
                if db_name not in to_update_yaml[entity]:
                    to_update_yaml[entity][db_name] = dbs[db_name]
                else:
                    for version in v["versions"]:
                        if version not in to_update_yaml[entity][db_name]["versions"]:
                            to_update_yaml[entity][db_name]["versions"][version] = v[
                                "versions"
                            ][version]

    write_yaml(to_update_yaml, _LOCAL_PATH)


def create_lndb() -> None:
    """If no ._lndb file, write ._current to ._lndb for lndb."""
    if not _LNDB_PATH.exists():
        shutil.copy2(_CURRENT_PATH, _LNDB_PATH)