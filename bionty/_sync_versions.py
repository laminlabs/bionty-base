from pathlib import Path
from typing import List, Literal, Tuple, Union

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
    new_defaults: Union[Tuple[str, str, str], List[Tuple[str, str, str]]],
    target: Literal["current", "lndb"] = "current",
) -> None:
    """Updates the _current.yaml file wih new user defaults.

    The _current.yaml stores the default databases and versions that Bionty accesses.
    This function overwrites the current defaults in the ._current.yaml file.

    Args:
        new_defaults: Triplets of (entity, database, version) tuples.
        target: The yaml file to update. Defaults to current
    """
    defaults = (
        load_yaml(_CURRENT_PATH) if target == "current" else load_yaml(_LNDB_PATH)
    )

    if isinstance(new_defaults, Tuple):  # type: ignore
        new_defaults = [new_defaults]  # type: ignore

    # TODO Validate whether new defaults are also available in the local.yaml
    for nd in new_defaults:
        entity = nd[0]
        new_db = nd[1]
        new_version = nd[2]

        defaults[entity] = {new_db: new_version}

    write_yaml(defaults, _CURRENT_PATH)


create_local(overwrite=False)
sync_yaml_format()
update_local()
create_current(overwrite=False)
create_lndb()
for default in ["current", "lndb"]:
    missing_defaults = _get_missing_defaults(source="local", defaults=default)  # type: ignore  # noqa: E501
    update_defaults(missing_defaults, target=default)  # type: ignore
