import warnings
from pathlib import Path
from typing import BinaryIO, Dict, List, Optional, Union

import pandas as pd
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

    def get_term(self, term):
        """Search an ontology by its id."""
        try:
            return super().get_term(term)
        except KeyError:
            return super().get_term(f"{self._prefix}{term.replace(':', '_')}")

    def to_df(
        self,
        source: Optional[str] = None,
        include_id_prefixes: Optional[Dict[str, List[str]]] = None,
    ):
        """Convert pronto.Ontology to a DataFrame with columns id, name, children."""
        df_values = []
        for term in self.terms():
            # skip terms without id or name and obsolete terms
            if (not term.id) or (not term.name) or term.obsolete:
                continue

            # term definition text
            definition = None if term.definition is None else term.definition.title()

            # concatenate synonyms into a string
            synonyms = "|".join(
                [i.description for i in term.synonyms if i.scope == "EXACT"]
            )
            if len(synonyms) == 0:
                synonyms = None  # type:ignore

            # get 1st degree children as a list
            subclasses = [
                s.id for s in term.subclasses(distance=1, with_self=False).to_set()
            ]

            df_values.append((term.id, term.name, definition, synonyms, subclasses))

        if include_id_prefixes and source in list(include_id_prefixes.keys()):
            flat_include_id_prefixes = {
                prefix1 for values in include_id_prefixes.values() for prefix1 in values  # type: ignore
            }
            df_values = list(
                filter(
                    lambda val: any(
                        val[0].startswith(prefix) for prefix in flat_include_id_prefixes
                    ),
                    df_values,
                )
            )

        df = pd.DataFrame(
            df_values,
            columns=["ontology_id", "name", "definition", "synonyms", "children"],
        ).set_index("ontology_id")

        # needed to avoid erroring in .lookup()
        df["name"].fillna("", inplace=True)

        return df
