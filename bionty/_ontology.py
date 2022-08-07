import warnings
from pathlib import Path
from typing import BinaryIO, Union

import pronto

from ._settings import check_dynamicdir_exists, settings


class Ontology(pronto.Ontology):
    """Interface with ontologies."""

    def __init__(
        self,
        handle: Union[str, Path, BinaryIO, None] = None,
        import_depth: int = -1,
        threads: Union[int, None] = None,
    ) -> None:
        warnings.filterwarnings("ignore", category=pronto.warnings.ProntoWarning)
        self.ontology = super().__init__(
            handle=handle, import_depth=import_depth, threads=threads
        )

    @check_dynamicdir_exists
    def write_obo(self, filename=None):
        if filename is None:
            filename = self.ontology.path.split("/")[-1].replace(".owl", ".obo")
            filepath = settings.dynamicdir / filename
        with open(filepath, "w") as f:
            f.write(self.ontology.dumps(format="obo"))

        return filepath
