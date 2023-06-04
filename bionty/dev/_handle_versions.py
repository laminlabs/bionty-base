import shutil
from pathlib import Path
from typing import Dict, List, Literal, Tuple

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

        current_data: Dict[str, Dict[str, Dict[str, str]]] = {}
        for bionty_entity, entity_data in versions.items():
            if bionty_entity == "version":
                continue

            current_data.setdefault(bionty_entity, {})

            # Take the top most option for the database and it's associated metadata
            database = list(entity_data.keys())[0]
            database_metadata = list(entity_data.values())[0]
            versions = database_metadata.get("versions", {})

            if versions:
                # convert to strings because lndb.yaml requires strings for lamindb compatbility
                latest_version = str(max(versions.keys()))

                for species in database_metadata["species"]:
                    current_data[bionty_entity].setdefault(species, {}).update(
                        {database: latest_version}
                    )

        write_yaml(current_data, _CURRENT_PATH)


def create_local(overwrite: bool = True) -> None:
    """If local.yaml doesn't exist, copy from versions.yaml and create it.

    Args:
        overwrite: Whether to overwrite the current local.yaml .
    """
    if not LOCAL_PATH.exists() or overwrite:
        versions = load_yaml(VERSIONS_PATH)
        write_yaml(versions, LOCAL_PATH)


def update_local() -> None:
    """Update local.yaml to add additional entries from the public versions.yaml table."""
    local = load_yaml(LOCAL_PATH)

    versions = load_yaml(VERSIONS_PATH)

    for key, value in versions.items():
        if key in local:
            if "versions" in local[key] and "versions" in value:
                local_versions = local[key]["versions"]
                versions = value["versions"]
                for version, info in versions.items():
                    if version not in local_versions:
                        local_versions[version] = info
            else:
                local[key] = value
        else:
            local[key] = value

    write_yaml(local, LOCAL_PATH)


def create_lndb() -> None:
    """If no ._lndb file, write ._current to ._lndb for lndb."""
    if not _LNDB_PATH.exists():
        shutil.copy2(_CURRENT_PATH, _LNDB_PATH)


def _get_missing_defaults(
    source: Literal["versions", "local"] = "local",
    defaults: Literal["current", "lndb"] = "current",
) -> List[Tuple[str, str, str, str]]:
    """Compares a version yaml file against a defaults yaml file and determines a diff.

    Args:
        source: The complete versions yaml file. One of "versions, "local".
                Defaults to "local".
        defaults: The current defaults yaml file. One of "current", "lndb".
                  Defaults to "current".

    Returns:
        A list of MissingDefault that can serve as input for `update_defaults`.
    """
    versions_yaml = (
        load_yaml(VERSIONS_PATH) if source == "versions" else load_yaml(LOCAL_PATH)
    )
    defaults_yaml = (
        load_yaml(_CURRENT_PATH) if defaults == "current" else load_yaml(_LNDB_PATH)
    )

    missing_defaults = []
    missing_entites = set(versions_yaml.keys()) - set(defaults_yaml.keys())
    missing_entites.remove("version")

    for entity in missing_entites:
        entity_content = list(versions_yaml.get(entity).items())
        for content in entity_content:
            database = content[0]
            versions_species = content[1]
            species: list[str] = versions_species.get("species", {})
            latest_version = list(versions_species.get("versions", {}).keys())[0]

            for spec in species:
                missing_defaults.append((entity, database, spec, latest_version))

    return missing_defaults
