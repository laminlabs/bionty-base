import warnings
from pathlib import Path
from typing import BinaryIO, Union

import pronto

from ._logger import logger
from ._settings import check_dynamicdir_exists, settings


class Ontology(pronto.Ontology):
    """Interface with ontologies."""

    def __init__(
        self,
        handle: Union[str, Path, BinaryIO, None] = None,
        import_depth: int = -1,
        threads: Union[int, None] = None,
        url: Union[str, None] = None,
    ) -> None:
        warnings.filterwarnings("ignore", category=pronto.warnings.ProntoWarning)
        if url is not None:
            logger.info("Downloading ontology for the first time might take a while...")
            handle = url
        super().__init__(handle=handle, import_depth=import_depth, threads=threads)

    @check_dynamicdir_exists
    def write_obo(self, filename: Union[str, None] = None):
        if filename is None:
            filename = self.path.split("/")[-1].replace(".owl", ".obo")
            filepath = settings.dynamicdir / filename
        with open(filepath, "wb") as f:
            self.dump(f, format="obo")

        return filepath
