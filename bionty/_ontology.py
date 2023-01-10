import warnings
from pathlib import Path
from typing import BinaryIO, Optional, Union

import pronto


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
        prefix: str = "",
    ) -> None:
        self._prefix = prefix
        warnings.filterwarnings("ignore", category=pronto.warnings.ProntoWarning)
        super().__init__(
            handle=handle, import_depth=import_depth, timeout=timeout, threads=threads
        )

    def write_obo(self):
        """Write ontology to dynamicdir/{filename}.obo file."""
        filepath = Path(self.path)
        filename = filepath.name.replace(".owl", ".obo")
        with open(filepath.parent / filename, "wb") as f:
            self.dump(f, format="obo")

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
