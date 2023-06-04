import os
import shutil
import tempfile
from pathlib import Path

from lamin_logger import logger

ROOT = Path(__file__).parent.parent / "versions"
VERSIONS_PATH = ROOT / "versions.yaml"
_CURRENT_PATH = ROOT / "._current.yaml"
_LNDB_PATH = ROOT / "._lndb.yaml"


def delete_yamls() -> None:
    for file_path in [VERSIONS_PATH, _CURRENT_PATH, _LNDB_PATH]:
        if os.path.exists(file_path):
            temp_dir = Path(tempfile.mkdtemp())
            new_file_path = temp_dir / file_path.name
            shutil.copy(file_path, new_file_path)
            logger.info(f"File '{file_path}' copied to '{new_file_path}'.")

            os.remove(file_path)
            logger.warning(f"Original file '{file_path}' successfully removed.")
        else:
            raise RuntimeError(f"File '{file_path}' does not exist.")
