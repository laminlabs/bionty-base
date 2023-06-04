import shutil
from pathlib import Path
from typing import Dict, Literal, Union

import pandas as pd

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

        df = parse_versions_yaml(source_path)
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

        write_yaml(current_dict, CURRENT_VERSIONS_PATH)


def update_local_from_versions_yaml():
    """Update LOCAL_VERSIONS_PATH to add additional entries from PUBLIC_VERSIONS_PATH."""
    pass


# def update_local() -> None:
#     """Update local.yaml to add additional entries from the public versions.yaml table."""
#     local = load_yaml(LOCAL_PATH)

#     versions = load_yaml(VERSIONS_PATH)

#     for key, value in versions.items():
#         if key in local:
#             if "versions" in local[key] and "versions" in value:
#                 local_versions = local[key]["versions"]
#                 versions = value["versions"]
#                 for version, info in versions.items():
#                     if version not in local_versions:
#                         local_versions[version] = info
#             else:
#                 local[key] = value
#         else:
#             local[key] = value

#     write_yaml(local, LOCAL_PATH)


# def _get_missing_defaults(
#     source: Literal["versions", "local"] = "local",
#     defaults: Literal["current", "lndb"] = "current",
# ) -> List[Tuple[str, str, str, str]]:
#     """Compares a version yaml file against a defaults yaml file and determines a diff.

#     Args:
#         source: The complete versions yaml file. One of "versions, "local".
#                 Defaults to "local".
#         defaults: The current defaults yaml file. One of "current", "lndb".
#                   Defaults to "current".

#     Returns:
#         A list of MissingDefault that can serve as input for `update_defaults`.
#     """
#     versions_yaml = (
#         load_yaml(VERSIONS_PATH) if source == "versions" else load_yaml(LOCAL_PATH)
#     )
#     defaults_yaml = (
#         load_yaml(_CURRENT_PATH) if defaults == "current" else load_yaml(_LNDB_PATH)
#     )

#     missing_defaults = []
#     missing_entites = set(versions_yaml.keys()) - set(defaults_yaml.keys())
#     missing_entites.remove("version")

#     for entity in missing_entites:
#         entity_content = list(versions_yaml.get(entity).items())
#         for content in entity_content:
#             database = content[0]
#             versions_species = content[1]
#             species: list[str] = versions_species.get("species", {})
#             latest_version = list(versions_species.get("versions", {}).keys())[0]

#             for spec in species:
#                 missing_defaults.append((entity, database, spec, latest_version))

#     return missing_defaults


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
