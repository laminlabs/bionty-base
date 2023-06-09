import os
from pathlib import Path
from typing import Dict, List, Literal, Union

from lamin_logger import logger
from pandas import DataFrame

from bionty._settings import settings
from bionty.dev._io import load_yaml, write_yaml

ROOT = Path(__file__).parent.parent / "sources"
PUBLIC_SOURCES_PATH = ROOT / "sources.yaml"

# hidden from the users
CURRENT_SOURCES_PATH = ROOT / ".currently_used_sources.yaml"
LAMINDB_SOURCES_PATH = ROOT / ".lamindb_currently_used_sources.yaml"

# Visible to the users and can be modified
LOCAL_VERSIONS_PATH = settings.versionsdir / "sources.local.yaml"

LAMINDB_INSTANCE_LOADED = os.path.exists(
    f"{os.environ['HOME']}/.lamin/current_instance.env"
)


def parse_sources_yaml(filepath: Union[str, Path]) -> DataFrame:
    """Parse values from sources yaml file into a DataFrame.

    Args:
        filepath: Path to the versions yaml file.
        return_df: Whether to return a Pandas DataFrame

    Returns:
        - entity
        - source_key
        - species
        - version
        - url
        - md5
        - source_name
        - source_website
    """
    import pandas as pd

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


def create_sources_local_yaml(overwrite: bool = True) -> None:
    """If LOCAL_VERSIONS_PATH doesn't exist, copy from PUBLIC_SOURCES_PATH and create it.

    Args:
        overwrite: Whether to overwrite the current LOCAL_VERSIONS_PATH.
    """
    if not LOCAL_VERSIONS_PATH.exists() or overwrite:
        public_df_records = parse_sources_yaml(PUBLIC_SOURCES_PATH).to_dict(  # type: ignore
            orient="records"
        )
        versions = add_records_to_existing_dict(public_df_records, {})
        versions_header = {"version": load_yaml(PUBLIC_SOURCES_PATH).get("version")}
        versions_header.update(versions)
        write_yaml(versions_header, LOCAL_VERSIONS_PATH)
        logger.success(f"Created {LOCAL_VERSIONS_PATH}!")


def create_currently_used_sources_yaml(
    overwrite: bool = True, source: Literal["versions", "local"] = "local"
) -> None:
    """Write the most recent version to the CURRENT_SOURCES_PATH .

    Takes the 1st source defined in the source.

    Args:
        overwrite: Whether to overwrite the CURRENT_SOURCES_PATH even if it exists already.
        source: The yaml source to use to create the CURRENT_SOURCES_PATH.
                Defaults to 'local'.
    """
    if not CURRENT_SOURCES_PATH.exists() or overwrite:
        source_path = (
            PUBLIC_SOURCES_PATH if source == "versions" else LOCAL_VERSIONS_PATH
        )

        write_yaml(parse_currently_used_sources(source_path), CURRENT_SOURCES_PATH)


def records_diff_btw_yamls(
    yamlpath1: Union[str, Path], yamlpath2: Union[str, Path]
) -> List:
    """Records in yaml1 but not yaml2."""
    public_df_records = parse_sources_yaml(yamlpath1).to_dict(orient="records")
    local_df_records = parse_sources_yaml(yamlpath2).to_dict(orient="records")
    additional_records = [i for i in public_df_records if i not in local_df_records]
    return additional_records


def update_local_from_public_sources_yaml() -> None:
    """Update LOCAL_VERSIONS_PATH to add additional entries from PUBLIC_SOURCES_PATH."""
    additional_records = records_diff_btw_yamls(
        PUBLIC_SOURCES_PATH, LOCAL_VERSIONS_PATH
    )
    if len(additional_records) > 0:
        updated_local_versions = add_records_to_existing_dict(
            additional_records, load_yaml(LOCAL_VERSIONS_PATH)
        )
        write_yaml(updated_local_versions, LOCAL_VERSIONS_PATH)
        logger.success(
            "New records found in the public sources.yaml, updated"
            f" {LOCAL_VERSIONS_PATH}!"
        )
        # update LOCAL_VERSIONS_PATH will always generate new CURRENT_SOURCES_PATH
        create_currently_used_sources_yaml(overwrite=True)


def parse_currently_used_sources(yaml: Union[str, Path, List[Dict]]) -> Dict:
    """Parse out the most recent versions from yaml."""
    if isinstance(yaml, (str, Path)):
        df = parse_sources_yaml(yaml)
        df_current = (
            df[["entity", "source_key", "species", "version"]]  # type: ignore
            .drop_duplicates(["entity", "species", "source_key"], keep="first")
            .groupby(["entity", "species", "source_key"], sort=False)
            .max()
        )
        records = df_current.reset_index().to_dict(orient="records")
    else:
        records = yaml

    current_dict: Dict = {}
    for kwargs in records:
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


def add_records_to_existing_dict(records: List[Dict], target_dict: Dict) -> Dict:
    """Add records to a versions yaml file."""
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
