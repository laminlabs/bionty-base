from bionty._compat.bionty_0_8_1 import update_yaml_unversionized_to_0_1
from bionty._settings import settings
from bionty.dev._io import load_yaml

_LOCAL_PATH = settings.versionsdir / "local.yaml"


def sync_yaml_format():
    versions = load_yaml(_LOCAL_PATH)

    # Unversionized to 0.1.0
    if "version" not in versions.keys():
        update_yaml_unversionized_to_0_1()