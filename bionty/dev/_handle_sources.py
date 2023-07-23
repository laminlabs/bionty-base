from pathlib import Path
from typing import Dict, List, Literal, Union

import pandas as pd
from lamin_utils import logger

from bionty._settings import settings
from bionty.dev._io import load_yaml, write_yaml

ROOT = Path(__file__).parent.parent / "sources"
PUBLIC_SOURCES = ROOT / "sources.yaml"

# hidden from the users
CURRENT_SOURCES = ROOT / ".current_sources.yaml"
LAMINDB_SOURCES = ROOT / ".lamindb_current_sources.yaml"

# Visible to the users and can be modified
LOCAL_SOURCES = settings.versionsdir / "sources_local.yaml"


def LAMINDB_INSTANCE_LOADED():
    is_loaded = False
    lnenv_filepath = Path.home() / ".lamin/current_instance.env"
    if lnenv_filepath.exists():
        with open(lnenv_filepath.as_posix(), "r") as f:
            is_loaded = "bionty" in f.read().split("schema_str=")[-1]
    return is_loaded


def reset_sources():
    """Reset local bionty sources file."""
    from importlib import reload

    import bionty

    def _confirm() -> bool:
        """Ask user to enter Y or N (case-insensitive).

        Returns:
            True if the answer is Y/y.
        """
        answer = ""
        while answer not in ["y", "n"]:
            answer = input(
                "Are you sure that you want to reset your local bionty sources? [Y/N]? "
            ).lower()
        return answer == "y"

    if _confirm():
        try:
            LOCAL_SOURCES.unlink()
            logger.success(f"Removed file: {LOCAL_SOURCES}.")
        except FileNotFoundError:
            pass
        try:
            CURRENT_SOURCES.unlink()
            logger.success(f"Removed file: {CURRENT_SOURCES}.")
        except FileNotFoundError:
            pass
        try:
            LAMINDB_SOURCES.unlink()
            logger.success(f"Removed file: {LAMINDB_SOURCES}.")
        except FileNotFoundError:
            pass

        reload(bionty)
        logger.info("Reloaded bionty!")


def create_or_update_sources_local_yaml(overwrite: bool = True) -> None:
    """If LOCAL_SOURCES doesn't exist, copy from PUBLIC_SOURCES and create it.

    Args:
        overwrite: Whether to overwrite the current LOCAL_SOURCES.
    """
    if not LOCAL_SOURCES.exists() or overwrite:
        public_df_records = parse_sources_yaml(PUBLIC_SOURCES).to_dict(  # type: ignore
            orient="records"
        )
        versions = add_records_to_existing_dict(public_df_records, {})
        versions_header = {"version": load_yaml(PUBLIC_SOURCES).get("version")}
        versions_header.update(versions)
        write_yaml(versions_header, LOCAL_SOURCES)
    else:
        update_local_from_public_sources_yaml()


def parse_sources_yaml(filepath: Union[str, Path] = PUBLIC_SOURCES) -> pd.DataFrame:
    """Parse values from sources yaml file into a DataFrame.

    Args:
        filepath: Path to the versions yaml file.

    Returns:
        - entity
        - source
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
        for source, species_source in sources.items():
            name = species_source.get("name", "")
            website = species_source.get("website", "")
            for species, versions in species_source.items():
                if species in ["name", "website"]:
                    continue
                for version_key, version_meta in versions.items():
                    row = (
                        entity,
                        source,
                        species,
                        str(version_key),
                        version_meta.get("url"),
                        version_meta.get("md5", ""),
                        name,
                        website,
                    )
                    all_rows.append(row)

    return pd.DataFrame(
        all_rows,
        columns=[
            "entity",
            "source",
            "species",
            "version",
            "url",
            "md5",
            "source_name",
            "source_website",
        ],
    )


def create_currently_used_sources_yaml(
    overwrite: bool = True, source: Literal["versions", "local"] = "local"
) -> None:
    """Write the most recent version to the CURRENT_SOURCES .

    Takes the 1st source defined in the source.

    Args:
        overwrite: Whether to overwrite the CURRENT_SOURCES even if it exists already.
        source: The yaml source to use to create the CURRENT_SOURCES.
                Defaults to 'local'.
    """
    if not CURRENT_SOURCES.exists() or overwrite:
        source_path = PUBLIC_SOURCES if source == "versions" else LOCAL_SOURCES

        write_yaml(parse_currently_used_sources(source_path), CURRENT_SOURCES)


def records_diff_btw_yamls(
    yamlpath1: Union[str, Path], yamlpath2: Union[str, Path]
) -> List:
    """Records in yaml1 but not yaml2."""
    public_df_records = parse_sources_yaml(yamlpath1).to_dict(orient="records")
    local_df_records = parse_sources_yaml(yamlpath2).to_dict(orient="records")
    additional_records = [
        record for record in public_df_records if record not in local_df_records
    ]

    return additional_records


def update_local_from_public_sources_yaml() -> None:
    """Update LOCAL_SOURCES to add additional entries from PUBLIC_SOURCES."""
    additional_records = records_diff_btw_yamls(PUBLIC_SOURCES, LOCAL_SOURCES)
    if len(additional_records) > 0:
        updated_local_versions = add_records_to_existing_dict(
            additional_records, load_yaml(LOCAL_SOURCES)
        )
        write_yaml(updated_local_versions, LOCAL_SOURCES)
        logger.success(
            f"New records found in the public sources.yaml, updated {LOCAL_SOURCES}!"
        )


def parse_currently_used_sources(yaml: Union[str, Path, List[Dict]]) -> Dict:
    """Parse out the most recent versions from yaml."""
    if isinstance(yaml, (str, Path)):
        df = parse_sources_yaml(yaml)
        df_current = (
            df[["entity", "source", "species", "version"]]  # type: ignore
            .drop_duplicates(["entity", "species", "source"], keep="first")
            .groupby(["entity", "species", "source"], sort=False)
            .max()
        )
        records = df_current.reset_index().to_dict(orient="records")
    else:
        records = yaml

    current_dict: Dict = {}
    for kwargs in records:
        entity, species, source, version = (
            kwargs["entity"],
            kwargs["species"],
            kwargs["source"],
            kwargs["version"],
        )
        if entity not in current_dict:
            current_dict[entity] = {}
        if species not in current_dict[entity]:
            current_dict[entity][species] = {source: version}
    return current_dict


def add_records_to_existing_dict(records: List[Dict], target_dict: Dict) -> Dict:
    """Add records to a versions yaml file."""
    for kwargs in records:
        entity, source, species, version = (
            kwargs["entity"],
            kwargs["source"],
            kwargs["species"],
            kwargs["version"],
        )
        if entity not in target_dict:
            target_dict[entity] = {}
        if source not in target_dict[entity]:
            target_dict[entity][source] = {
                species: {version: {"url": kwargs["url"], "md5": kwargs["md5"]}}
            }
            target_dict[entity][source].update(
                {"name": kwargs["source_name"], "website": kwargs["source_website"]}
            )
        if species not in target_dict[entity][source]:
            target_dict[entity][source][species] = {
                version: {"url": kwargs["url"], "md5": kwargs["md5"]}
            }
        if version not in target_dict[entity][source][species]:
            target_dict[entity][source][species][version] = {
                "url": kwargs["url"],
                "md5": kwargs["md5"],
            }
    return target_dict
