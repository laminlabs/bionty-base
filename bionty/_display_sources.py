from pathlib import Path

import pandas as pd

from bionty.dev._handle_sources import LAMINDB_INSTANCE_LOADED
from bionty.dev._io import load_yaml

ROOT_DIR = Path(__file__).parent.resolve()


def display_available_sources() -> pd.DataFrame:
    """Displays all available sources.

    Examples:
        >>> import bionty as bt
        >>> bt.display_available_sources()
    """
    from .dev._handle_sources import LOCAL_VERSIONS_PATH, parse_sources_yaml

    return parse_sources_yaml(LOCAL_VERSIONS_PATH).set_index("entity")  # type: ignore


# This function naming is consistent with the `currently_used` field in BiontySource SQL table
# Do not rename!
def display_currently_used_sources() -> pd.DataFrame:
    """Displays all currently used sources.

    Active version is unique for entity + species.

    Examples:
        >>> import bionty as bt
        >>> bt.display_currently_used_sources()
    """
    from .dev._handle_sources import CURRENT_SOURCES_PATH, LAMINDB_SOURCES_PATH

    VERSIONS_FILE_PATH = (
        LAMINDB_SOURCES_PATH if LAMINDB_INSTANCE_LOADED else CURRENT_SOURCES_PATH
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
