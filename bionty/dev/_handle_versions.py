import shutil
from pathlib import Path
from typing import List, Literal, Tuple

import pandas as pd

from bionty._settings import settings
from bionty.dev._io import load_yaml, write_yaml

ROOT = Path(__file__).parent.parent / "versions"
VERSIONS_PATH = ROOT / "versions.yaml"
_CURRENT_PATH = ROOT / "._current.yaml"
_LNDB_PATH = ROOT / "._lndb.yaml"

LOCAL_PATH = settings.versionsdir / "local.yaml"


def latest_db_version(db: str) -> str:
    """Lookup the latest version of a source.

    Args:
        db: The source to look up the version for.

    Returns:
        The version of the source. Usually a date.
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

    Takes the 1st source defined in the source.

    Args:
        overwrite: Whether to overwrite the _current.yaml even if it exists already.
        source: The yaml source to use to create the _current.yaml .
                Defaults to 'local'.
    """
    if not _CURRENT_PATH.exists() or overwrite:
        versions = (
            load_yaml(VERSIONS_PATH) if source == "versions" else load_yaml(LOCAL_PATH)
        )

        def _write_current_yaml(versions):
            _current = {}
            for name, db_versions in versions.items():
                if name == "version":
                    continue
                # this will only take the 1st db if multiple exists for the same entity
                db = next(iter(db_versions))
                versions = db_versions.get(db).get("versions")
                version = str(sorted(versions.keys(), reverse=True)[0])
                _current[name] = {db: version}
            return _current

        _current = _write_current_yaml(versions)
        write_yaml(_current, _CURRENT_PATH)


def create_local(overwrite: bool = True) -> None:
    """If local.yaml doesn't exist, copy from versions.yaml and create it.

    Args:
        overwrite: Whether to overwrite the current local.yaml .
    """
    if not LOCAL_PATH.exists() or overwrite:
        versions = load_yaml(VERSIONS_PATH)
        # convert all non string keys to strings
        local_versions = {}
        for entity, dbs in versions.items():
            local_versions[entity] = versions[entity]
            if entity == "version":
                continue
            for db_name, v in dbs.items():
                # list is needed here to avoid dict key change error
                for version in list(v["versions"]):
                    if isinstance(version, str):
                        continue
                    local_versions[entity][db_name]["versions"][
                        str(version)
                    ] = local_versions[entity][db_name]["versions"].pop(version)

        write_yaml(local_versions, LOCAL_PATH)


def update_local() -> None:
    """Update local.yaml to add additional entries from the public versions.yaml table."""
    to_update_yaml = load_yaml(LOCAL_PATH)

    versions = load_yaml(VERSIONS_PATH)

    for entity, dbs in versions.items():
        if entity == "version":
            continue
        if entity not in to_update_yaml:
            to_update_yaml[entity] = versions[entity]
        else:
            for db_name, v in dbs.items():
                if db_name not in to_update_yaml[entity]:
                    to_update_yaml[entity][db_name] = dbs[db_name]
                else:
                    for version in v["versions"]:
                        if (
                            str(version)
                            not in to_update_yaml[entity][db_name]["versions"]
                        ):
                            to_update_yaml[entity][db_name]["versions"][version] = v[
                                "versions"
                            ][version]

    write_yaml(to_update_yaml, LOCAL_PATH)


def create_lndb() -> None:
    """If no ._lndb file, write ._current to ._lndb for lndb."""
    if not _LNDB_PATH.exists():
        shutil.copy2(_CURRENT_PATH, _LNDB_PATH)


def _get_missing_defaults(
    source: Literal["versions", "local"] = "local",
    defaults: Literal["current", "lndb"] = "current",
) -> List[Tuple[str, str, str]]:
    """Compares a version yaml file against a defaults yaml file and determines a diff.

    Args:
        source: The complete versions yaml file. One of "versions, "local".
                Defaults to "local".
        defaults: The current defaults yaml file. One of "current", "lndb".
                  Defaults to "current".

    Returns:
        A list of tuples in the form of [(Bionty class, source, version)] that
        can serve as input for `update_defaults`.
    """
    versions_yaml = (
        load_yaml(VERSIONS_PATH) if source == "versions" else load_yaml(LOCAL_PATH)
    )
    defaults_yaml = (
        load_yaml(_CURRENT_PATH) if defaults == "current" else load_yaml(_LNDB_PATH)
    )

    formatted_missing = []
    missing_entites = set(versions_yaml.keys()) - set(defaults_yaml.keys())
    missing_entites.remove("version")

    for entity in missing_entites:
        database, _ = list(versions_yaml.get(entity).items())[0]
        version = str(
            list(versions_yaml.get(entity, {}).get(database, {}).get("versions", {}))[0]
        )
        formatted_missing.append((entity, database, version))

    return formatted_missing
