from filelock import FileLock  # type: ignore

from ._compat.update_yaml_format import sync_yaml_format
from .dev._handle_versions import (
    ROOT,
    create_current_versions_yaml,
    create_lamindb_setup_yaml,
    create_local_versions_yaml,
    update_local_from_versions_yaml,
)

# Make this code safe when running bionty from multiple processes
with FileLock(ROOT / "bionty.lock"):
    create_local_versions_yaml(overwrite=False)
    sync_yaml_format()
    update_local_from_versions_yaml()
    create_current_versions_yaml(overwrite=False)
    create_lamindb_setup_yaml(overwrite=False)
