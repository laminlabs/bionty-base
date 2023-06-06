import os
from pathlib import Path

import pandas as pd

from bionty.dev._io import load_yaml

ROOT_DIR = Path(__file__).parent.resolve()


def display_available_versions() -> pd.DataFrame:
    """Displays all available entities and versions.

    Examples:
        >>> import bionty as bt
        >>> bt.display_available_versions()
    """
    from .dev._handle_versions import LOCAL_VERSIONS_PATH, parse_versions_yaml

    return parse_versions_yaml(LOCAL_VERSIONS_PATH).set_index("entity")  # type: ignore


def display_active_versions() -> pd.DataFrame:
    """Displays all currently set as default entities and versions.

    Active version is unique for entity + species.

    Examples:
        >>> import bionty as bt
        >>> bt.display_active_versions()
    """
    from .dev._handle_versions import CURRENT_VERSIONS_PATH, LAMINDB_VERSIONS_PATH

    VERSIONS_FILE_PATH = (
        LAMINDB_VERSIONS_PATH
        if os.getenv("LAMINDB_INSTANCE_LOADED") == 1
        else CURRENT_VERSIONS_PATH
    )

    versions = load_yaml(VERSIONS_FILE_PATH.resolve())

    df_rows = []
    for bionty_class, bionty_class_data in versions.items():
        for species, species_data in bionty_class_data.items():
            for source_key, version in species_data.items():
                df_rows.append(
                    {
                        "entity": bionty_class,
                        "species": species,
                        "source_key": source_key,
                        "version": version,
                    }
                )

    return pd.DataFrame(df_rows).set_index("entity")
