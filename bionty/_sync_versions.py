from pathlib import Path
from typing import Literal, Sequence, Tuple

from filelock import FileLock  # type: ignore

from ._compat.update_yaml_format import sync_yaml_format
from ._settings import settings
from .dev._handle_versions import (
    _get_missing_defaults,
    create_current,
    create_lndb,
    create_local,
    update_local,
)
from .dev._io import load_yaml, write_yaml

ROOT = Path(__file__).parent / "versions"
VERSIONS_PATH = ROOT / "versions.yaml"
_CURRENT_PATH = ROOT / "._current.yaml"
_LNDB_PATH = ROOT / "._lndb.yaml"

_LOCAL_PATH = settings.versionsdir / "local.yaml"


def update_defaults(
    new_defaults: Sequence[Tuple[str, str, str, str]],
    target: Literal["current", "lndb"] = "current",
) -> None:
    """Updates the _current.yaml file with new user defaults.

    The _current.yaml stores the default databases and versions that Bionty accesses.
    This function overwrites the current defaults in the ._current.yaml file.

    Args:
        new_defaults: List of Tuples in order Bionty Entity, Source, Species, version
        target: The yaml file to update. Defaults to current
    """
    defaults = (
        load_yaml(_CURRENT_PATH) if target == "current" else load_yaml(_LNDB_PATH)
    )

    for nd in new_defaults:
        entity = nd[0]
        source = nd[1]
        species = nd[2]
        latest_version = nd[3]

        if entity not in defaults:
            defaults[entity] = {}

        if species not in defaults[entity]:  # type: ignore
            defaults[entity][species] = {}  # type: ignore

            defaults[entity][species][source] = latest_version  # type: ignore

    if target == "current":
        write_yaml(defaults, _CURRENT_PATH)
    else:
        write_yaml(defaults, _LNDB_PATH)


# Make this code safe when running bionty from multiple processes
with FileLock(ROOT / "bionty.lock"):
    create_local(overwrite=False)
    sync_yaml_format()
    update_local()
    create_current(overwrite=False)
    create_lndb()
    for default in ["current", "lndb"]:
        missing_defaults = _get_missing_defaults(source="local", defaults=default)  # type: ignore  # noqa: E501
        update_defaults(missing_defaults, target=default)  # type: ignore
