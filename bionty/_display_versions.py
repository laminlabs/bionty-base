import os
from pathlib import Path
from typing import Optional

import pandas as pd
from rich.console import Console
from rich.table import Table

from bionty._settings import settings
from bionty.dev._io import load_yaml

console = Console()

ROOT_DIR = Path(__file__).parent.resolve()


def display_available_versions(
    return_df: bool = False,
) -> Optional[pd.DataFrame]:  # pragma: no cover
    """Displays all available entities and versions in a Rich table.

    Args:
        return_df: Whether to return a Pandas DataFrame containing the available versions. Defaults to False.
    """
    VERSIONS_FILE_PATH = (settings.versionsdir / "local.yaml").resolve()
    versions = load_yaml(VERSIONS_FILE_PATH)

    table = Table(title="Available versions")

    table.add_column("Ontology", justify="right", style="cyan", no_wrap=True)
    table.add_column("URL", justify="right", style="cyan", no_wrap=True)
    table.add_column("Bionty Entity", justify="right", style="cyan", no_wrap=True)
    table.add_column("Database key", justify="right", style="cyan", no_wrap=True)
    table.add_column("All versions", justify="right", style="cyan", no_wrap=True)

    df_rows = []
    for entity, db_to_version in versions.items():
        if entity == "version":
            continue
        for db, _to_versions_url in db_to_version.items():
            versions = ""
            _ontology_name = _to_versions_url["name"]
            _ontology_url = _to_versions_url["website"]
            for version_str, url_md5 in _to_versions_url["versions"].items():
                versions += str(version_str) + "\n"

                # Compatibility code for old local.yml files that may not yet have md5s
                if len(url_md5) > 1:
                    url = url_md5[0]
                else:
                    url = url_md5

                df_rows.append(
                    {
                        "Ontology": _ontology_name,
                        "URL": url,
                        "Bionty Entity": entity,
                        "Database key": db,
                        "All versions": str(version_str),
                    }
                )
                table.add_row(_ontology_name, _ontology_url, entity, db, versions)

    if return_df:
        df = pd.DataFrame(df_rows)
        return df

    console.print(table)
    return None


def display_active_versions(
    return_df: bool = False,
) -> Optional[pd.DataFrame]:  # pragma: no cover
    """Displays all currently set as default entities and versions in a Rich table.

    Args:
        return_df: Whether to return a Pandas DataFrame containing the available versions. Defaults to False.
    """
    version_table = (
        "._lndb.yaml" if os.getenv("LAMINDB_INSTANCE_LOADED") == 1 else "._current.yaml"
    )

    VERSIONS_FILE_PATH = Path(f"{ROOT_DIR}/versions/{version_table}").resolve()
    versions = load_yaml(VERSIONS_FILE_PATH.resolve())

    table = Table(title=f"Currently used versions in {version_table}")

    table.add_column("Entity", justify="right", style="cyan", no_wrap=True)
    table.add_column("Database", justify="right", style="cyan", no_wrap=True)
    table.add_column("Version", justify="right", style="cyan", no_wrap=True)

    df_rows = []
    for entity, db_to_version in versions.items():
        for db, version in db_to_version.items():
            df_rows.append({"Entity": entity, "Database": db, "Version": str(version)})
            table.add_row(entity, db, str(version))

    if return_df:
        df = pd.DataFrame(df_rows)
        return df

    console.print(table)
    return None
