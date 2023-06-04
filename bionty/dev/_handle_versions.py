import shutil
from pathlib import Path
from typing import Dict, List, Literal, Union

from lamin_logger import logger

from bionty._settings import settings
from bionty.dev._io import load_yaml, write_yaml

ROOT = Path(__file__).parent.parent / "versions"
PUBLIC_VERSIONS_PATH = ROOT / "versions.yaml"

# hidden from the users
CURRENT_VERSIONS_PATH = ROOT / ".current_bionty_versions.yaml"
LAMINDB_VERSIONS_PATH = ROOT / ".lamindb_setup.yaml"

# Visible to the users and can be modified
LOCAL_VERSIONS_PATH = settings.versionsdir / "local_bionty_versions.yaml"


def parse_versions_yaml(filepath: Union[str, Path], return_df=True):
    """Parse values from versions yaml file into a DataFrame.

    - entity
    - source_key
    - species
    - version
    - url
    - md5
    - source_name
    - source_website
    """
    all_rows = []
    for entity, sources in load_yaml(filepath).items():
        if entity == "version":
            continue
        for source_key, species_source in sources.items():
            name = species_source.get("name", "")
            website = species_source.get("website", "")
            for species, versions in species_source.items():
                if species in ["name", "website"]:
                    continue
                for version_key, version_meta in versions.items():
                    row = (
                        entity,
                        source_key,
                        species,
                        str(version_key),
                        version_meta.get("source"),
                        version_meta.get("md5", ""),
                        name,
                        website,
                    )
                    all_rows.append(row)

    if return_df:
        import pandas as pd

        return pd.DataFrame(
            all_rows,
            columns=[
                "entity",
                "source_key",
                "species",
                "version",
                "url",
                "md5",
                "source_name",
                "source_website",
            ],
        )

    return all_rows


def create_local_versions_yaml(overwrite: bool = True) -> None:
    """If local_bionty_versions.yaml doesn't exist, copy from versions.yaml and create it.

    Args:
        overwrite: Whether to overwrite the current local_bionty_versions.yaml .
    """
    if not LOCAL_VERSIONS_PATH.exists() or overwrite:
        versions = load_yaml(PUBLIC_VERSIONS_PATH)
        write_yaml(versions, LOCAL_VERSIONS_PATH)


def create_lamindb_setup_yaml(overwrite: bool = True) -> None:
    """Create .lamindb_setup.yaml file from .

    Args:
        overwrite: Whether to overwrite the current lamindb_setup.yaml .
    """
    if not LAMINDB_VERSIONS_PATH.exists() or overwrite:
        shutil.copy2(CURRENT_VERSIONS_PATH, LAMINDB_VERSIONS_PATH)


def create_current_versions_yaml(
    overwrite: bool = True, source: Literal["versions", "local"] = "local"
) -> None:
    """Write the most recent version to the current_bionty_versions.yaml .

    Takes the 1st source defined in the source.

    Args:
        overwrite: Whether to overwrite the current_bionty_versions.yaml even if it exists already.
        source: The yaml source to use to create the _current.yaml .
                Defaults to 'local'.
    """
    if not CURRENT_VERSIONS_PATH.exists() or overwrite:
        source_path = (
            PUBLIC_VERSIONS_PATH if source == "versions" else LOCAL_VERSIONS_PATH
        )

        write_yaml(parse_current_versions(source_path), CURRENT_VERSIONS_PATH)


def update_local_from_versions_yaml():
    """Update LOCAL_VERSIONS_PATH to add additional entries from PUBLIC_VERSIONS_PATH."""
    public_df_records = parse_versions_yaml(PUBLIC_VERSIONS_PATH).to_dict(
        orient="records"
    )
    local_df_records = parse_versions_yaml(LOCAL_VERSIONS_PATH).to_dict(
        orient="records"
    )
    additional_records = [i for i in public_df_records if i not in local_df_records]
    if len(additional_records) > 0:
        updated_local_versions = add_records_to_versions_yaml(
            additional_records, LOCAL_VERSIONS_PATH
        )
        write_yaml(updated_local_versions, LOCAL_VERSIONS_PATH)
        logger.success(
            "New records found in the public version.yaml, updated"
            f" {LOCAL_VERSIONS_PATH}!"
        )
        # update LOCAL_VERSIONS_PATH will always generate new CURRENT_VERSIONS_PATH
        create_current_versions_yaml(overwrite=True)
        create_lamindb_setup_yaml(overwrite=True)


def parse_current_versions(yamlpath: Union[str, Path]):
    """Parse out the most recent versions from yaml."""
    df = parse_versions_yaml(yamlpath)
    df_current = (
        df[["entity", "source_key", "species", "version"]]
        .drop_duplicates(["entity", "species", "source_key"], keep="first")
        .groupby(["entity", "species", "source_key"], sort=False)
        .max()
    )

    current_dict: Dict = {}
    for kwargs in df_current.reset_index().to_dict(orient="records"):
        entity, species, source_key, version = (
            kwargs["entity"],
            kwargs["species"],
            kwargs["source_key"],
            kwargs["version"],
        )
        if entity not in current_dict:
            current_dict[entity] = {}
        if species not in current_dict[entity]:
            current_dict[entity][species] = {source_key: version}
    return current_dict


def add_records_to_versions_yaml(records: List[Dict], yaml_filepath):
    """Add records to a versions yaml file."""
    target_dict = load_yaml(yaml_filepath)
    for kwargs in records:
        entity, source_key, species, version = (
            kwargs["entity"],
            kwargs["source_key"],
            kwargs["species"],
            kwargs["version"],
        )
        if entity not in target_dict:
            target_dict[entity] = {}
        if source_key not in target_dict[entity]:
            target_dict[entity][source_key] = {
                species: {version: {"source": kwargs["url"], "md5": kwargs["md5"]}}
            }
            target_dict[entity][source_key].update(
                {"name": kwargs["source_name"], "website": kwargs["source_website"]}
            )
        if species not in target_dict[entity][source_key]:
            target_dict[entity][source_key][species] = {
                version: {"source": kwargs["url"], "md5": kwargs["md5"]}
            }
        if version not in target_dict[entity][source_key][species]:
            target_dict[entity][source_key][species][version] = {
                "source": kwargs["url"],
                "md5": kwargs["md5"],
            }
    return target_dict
