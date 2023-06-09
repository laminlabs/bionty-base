from filelock import FileLock  # type: ignore

from ._compat.update_yaml_format import sync_yaml_format
from .dev._handle_sources import (
    ROOT,
    create_currently_used_sources_yaml,
    create_sources_local_yaml,
    update_local_from_public_sources_yaml,
)

# Make this code safe when running bionty from multiple processes
with FileLock(ROOT / "bionty.lock"):
    create_sources_local_yaml(overwrite=False)
    sync_yaml_format()
    update_local_from_public_sources_yaml()
    create_currently_used_sources_yaml(overwrite=False)
