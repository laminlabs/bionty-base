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
    return_df: bool = True,
) -> Optional[pd.DataFrame]:  # pragma: no cover
    """Displays all available entities and versions in a Rich table.

    Args:
        return_df: Whether to return a Pandas DataFrame containing the available versions. Defaults to False.

    Examples:
        >>> import bionty as bt
        >>> bt.display_available_versions()
    """
    VERSIONS_FILE_PATH = (settings.versionsdir / "local.yaml").resolve()
    versions = load_yaml(VERSIONS_FILE_PATH)

    table = Table(title="Available versions")

    table.add_column("Bionty class", justify="right", style="cyan", no_wrap=True)
    table.add_column("Species", justify="right", style="cyan", no_wrap=True)
    table.add_column("Source key", justify="right", style="cyan", no_wrap=True)
    table.add_column("Version", justify="right", style="cyan", no_wrap=True)
    table.add_column("Ontology", justify="right", style="cyan", no_wrap=True)
    table.add_column("URL", justify="right", style="cyan", no_wrap=True)

    df_rows = []
    for entity, db_to_version in versions.items():
        if entity == "version":
            continue
        for db, db_content in db_to_version.items():
            species = "\n".join(db_content.get("species", {}))
            name = db_content.get("name", {})
            url = db_content.get("website", {})
            versions = "\n".join(
                list(map(str, list(db_content.get("versions", {}).keys())))
            )

            df_rows.append(
                {
                    "Bionty class": entity,
                    "Species": species,
                    "Source key": db,
                    "Version": versions,
                    "Ontology": name,
                    "URL": url,
                }
            )

            table.add_row(entity, species, db, versions, name, url)

    if return_df:
        df = pd.DataFrame(df_rows).set_index(["Bionty class", "Source key"])
        df = df.replace("\n", ",", regex=True)
        return df

    console.print(table)
    return None


def display_active_versions(
    return_df: bool = True,
) -> Optional[pd.DataFrame]:  # pragma: no cover
    """Displays all currently set as default entities and versions in a Rich table.

    Args:
        return_df: Whether to return a Pandas DataFrame containing the available versions. Defaults to False.

    Examples:
        >>> import bionty as bt
        >>> bt.display_active_versions()
    """
    version_table = (
        "._lndb.yaml" if os.getenv("LAMINDB_INSTANCE_LOADED") == 1 else "._current.yaml"
    )

    VERSIONS_FILE_PATH = Path(f"{ROOT_DIR}/versions/{version_table}").resolve()
    versions = load_yaml(VERSIONS_FILE_PATH.resolve())

    table = Table(title=f"Currently used versions in {version_table}")

    table.add_column("Bionty class", justify="right", style="cyan", no_wrap=True)
    table.add_column("Species", justify="right", style="cyan", no_wrap=True)
    table.add_column("Source key", justify="right", style="cyan", no_wrap=True)
    table.add_column("Version", justify="right", style="cyan", no_wrap=True)

    df_rows = []
    for bionty_class, bionty_class_data in versions.items():
        for species, species_data in bionty_class_data.items():
            for source_key, version in species_data.items():
                df_rows.append(
                    {
                        "Bionty class": bionty_class,
                        "Species": species,
                        "Source key": source_key,
                        "Version": version,
                    }
                )

                table.add_row(bionty_class, species, source_key, str(version))

    if return_df:
        df = pd.DataFrame(df_rows).set_index("Bionty class")
        return df

    console.print(table)
    return None
