import tempfile
from importlib import reload
from pathlib import Path

from lamin_logger import logger

import bionty
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
            logger.warning(
                "Outdated 'local.yaml' detected. Previous local.yaml is saved to"
                f" {Path(tempfile.gettempdir())}/local.yamlPlease contact Lamin if you"
                " were using customized ontology sources! Reimported Bionty."
            )
            reload(bionty)
            logger.success("Migrated to the latest yaml version!")
        except RuntimeError:
            logger.warning(
                "Unable to reset yaml files. Ensure that you are using at least Bionty"
                " 0.17.0 ."
            )
