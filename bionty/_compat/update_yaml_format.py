from importlib import reload

from lamin_logger import logger

import bionty
from bionty._compat.bionty_0_8_1 import update_yaml_from_unversionized_to_0_1
from bionty._compat.bionty_0_17_0 import delete_yamls
from bionty._settings import settings
from bionty.dev._io import load_yaml

_LOCAL_PATH = settings.versionsdir / "local.yaml"


def sync_yaml_format():
    try:
        versions = load_yaml(_LOCAL_PATH)
    except FileNotFoundError:
        return

    # Unversionized to 0.1.0
    if "version" not in versions.keys():
        logger.warning(
            "Detected unversionized yaml file. Upgrading to 0.1.0 yaml structure."
        )
        update_yaml_from_unversionized_to_0_1()
    # 0.1.0 to 0.2.0
    elif versions["version"] == "0.1.0":
        try:
            temp_dir = delete_yamls()
            logger.warning(
                "Outdated yaml files detected. Previous yaml files have been moved to"
                f" {temp_dir}! Please contact Lamin if you were using customized"
                " ontology sources!"
            )
            reload(bionty)
            logger.success("Migrated to the latest yaml version 0.2.0!")
        except RuntimeError:
            logger.error("Unable to reset yaml files. Please install 'bionty>=0.17.0'!")
