from filelock import FileLock  # type: ignore

from ._compat.update_yaml_format import sync_yaml_format
from .dev._handle_sources import (
    ROOT,
    create_currently_used_sources_yaml,
    create_or_update_sources_local_yaml,
)

# Make this code safe when running bionty from multiple processes
with FileLock(ROOT / "bionty.lock"):
    create_or_update_sources_local_yaml(overwrite=False)
    # always generate a new CURRENT_SOURCES file
    create_currently_used_sources_yaml(overwrite=True)
    sync_yaml_format()
