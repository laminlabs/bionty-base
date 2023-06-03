from lamin_logger import logger

from bionty._compat.bionty_0_8_1 import update_yaml_from_unversionized_to_0_1
from bionty._compat.bionty_0_16_0 import delete_yamls
from bionty._settings import settings
from bionty.dev._io import load_yaml

_LOCAL_PATH = settings.versionsdir / "local.yaml"


def sync_yaml_format():
    versions = load_yaml(_LOCAL_PATH)

    # Unversionized to 0.1.0
    if "version" not in versions.keys():
        logger.warning(
            "Detected unversionized yaml file. Upgrading to 0.1.0 yaml structure."
        )
        update_yaml_from_unversionized_to_0_1()
    # 0.1.0 to 0.2.0
    elif versions["version"] == "0.1.0":
        try:
            delete_yamls()
        except RuntimeError:
            logger.warning(
                "Unable to reset yaml files. Ensure that they are up to date and of at"
                " least version 0.2.0."
            )
        raise RuntimeError(
            "local.yaml version 0.1.0 detected. Moved existing yaml to a temporary"
            " directory and deleted the original yaml files.Please import Bionty again"
            " to regenerate the yaml files with the latest syntax.We have also reset"
            " your defaults. We are very sorry for the inconvenience."
        )
