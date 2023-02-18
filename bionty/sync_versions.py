import shutil
from pathlib import Path
from typing import Any, Dict, Literal

from .dev._io import load_yaml, write_yaml

ROOT = Path(__file__).parent / "versions"
VERSIONS_PATH = ROOT / "versions.yaml"
_LOCAL_PATH = ROOT / "_local.yaml"
_CURRENT_PATH = ROOT / "_current.yaml"
_LNDB_PATH = ROOT / "_lndb.yaml"


def create_current(
    overwrite: bool = True, source: Literal["versions", "local"] = "versions"
) -> None:
    """Writes the most recent version to the _current.yaml .

    Args:
        overwrite: Whether to overwrite the _current.yaml even if it exists already.
        source: The yaml source to use to create the _current.yaml for.
    """
    if not _CURRENT_PATH.exists() or overwrite:
        if source == "versions":
            versions = load_yaml(VERSIONS_PATH)
        else:
            versions = load_yaml(_LOCAL_PATH)

        def write_current_yaml(versions):
            _current = {}
            for name, db_versions in versions.items():
                # this will only take the 1st db if multiple exists for the same entity
                db = next(iter(db_versions))
                versions = db_versions.get(db).get("versions")
                version = str(sorted(versions.keys(), reverse=True)[0])
                _current[name] = {db: version}
            return _current

        _current = write_current_yaml(versions)
        write_yaml(_current, _CURRENT_PATH)


def write_local_yaml(versions):
    """Make sure version keys are strings."""
    _local = {}

    for name, db_versions in versions.items():
        db = next(iter(db_versions))
        versions = db_versions.get(db).get("versions")
        _local[name] = {db: {"versions": {}}}
        for version, version_url in versions.items():
            _local[name][db]["versions"][str(version)] = version_url

    write_yaml(_local, _LOCAL_PATH)


def create_local(overwrite: bool = True) -> None:
    """If _local.yaml doesn't exist, copy from versions.yaml and create it.

    Args:
        overwrite: Whether to overwrite the current _local.yaml .
    """
    if not _LOCAL_PATH.exists() or overwrite:
        versions = load_yaml(VERSIONS_PATH)

        write_local_yaml(versions)


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

    write_local_yaml(to_update_yaml)


def create_lndb() -> None:
    """If no _lndb file, write _current to _lndb for lndb."""
    if not _LNDB_PATH.exists():
        shutil.copy2(_CURRENT_PATH, _LNDB_PATH)


create_local(overwrite=False)
_local = load_yaml(_LOCAL_PATH)
update_local(_local)
create_current(overwrite=False)
create_lndb()
