import warnings
from pathlib import Path
from typing import BinaryIO, Optional, Union

import pronto

from ._logger import logger
from ._settings import check_dynamicdir_exists, settings


class Ontology(pronto.Ontology):
    """Interface with ontologies via pronto.

    Also see: https://pronto.readthedocs.io/en/stable/api/pronto.Ontology.html

    Args:
        handle: Path to an ontology file.
        import_depth: The maximum depth of imports to resolve in the ontology tree.
        timeout: The timeout in seconds to use when performing network I/O.
        threads: The number of threads to use when parsing.
        url: The url of ontology.
        prefix: Dev only -> prefix for get_term.
    """

    def __init__(
        self,
        handle: Union[str, Path, BinaryIO, None] = None,
        import_depth: int = -1,
        timeout: int = 100,
        threads: Optional[int] = None,
        url: Optional[str] = None,
        prefix: Optional[str] = None,
        filename: Optional[str] = None,
    ) -> None:
        self._prefix = "" if prefix is None else prefix
        warnings.filterwarnings("ignore", category=pronto.warnings.ProntoWarning)
        if url is not None:
            logger.info("Downloading ontology for the first time might take a while...")
            handle = url
        super().__init__(
            handle=handle, import_depth=import_depth, timeout=timeout, threads=threads
        )
        if url is not None:
            self.write_obo(filename=filename)

    @check_dynamicdir_exists
    def write_obo(self, filename: Optional[str] = None):
        """Write ontology to dynamicdir/{filename}.obo file."""
        if filename is None:
            filename = self.path.split("/")[-1].replace(".owl", ".obo")
        filepath = settings.dynamicdir / filename
        with open(filepath, "wb") as f:
            self.dump(f, format="obo")

        return filepath

    def get_term(self, term):
        """Search an ontology by its id."""
        try:
            return super().get_term(term)
        except KeyError:
            return super().get_term(f"{self._prefix}{term.replace(':', '_')}")

    def _list_subclasses(self, term, distance=1, with_self=False):
        """Subclasses of a term."""
        termclass = self.get_term(term)
        return list(termclass.subclasses(distance=distance, with_self=with_self))
