import logging as logg
from functools import cached_property
from pathlib import Path
from typing import Iterable, Union

import pandas as pd

from ._settings import format_into_dataframe


class Ontology:
    """Ontology manager built on Owlready2.

    Args:
        base_iri: (Internationalized Resource Identifier) RDF/XML, OWL/XML or NTriples format # noqa
        load: Whether to load ontology
    """

    def __init__(self, base_iri: Union[str, Path], load: bool = True) -> None:
        from owlready2 import get_ontology

        if load:
            self._onto = get_ontology(base_iri).load()
        else:
            self._onto = get_ontology(base_iri)

    @property
    def onto(self):
        """owlready2 ontology object."""
        return self._onto

    @cached_property
    def onto_dict(self) -> dict:
        """Keyed by name, valued by label."""
        return {i.name: i.label[0] for i in self.onto.classes()}

    @cached_property
    def classes(self) -> dict:
        """Indexed classes, owlready2 ThingClass object."""
        return {i.name: i for i in self.onto.classes()}

    def search(self, data: Iterable[str], id=False):
        """Search in ontology labels.

        Args:
            data: search patterns
            id: whether to search by the id

        Returns:
            A list of ontology names
        """
        res = {}
        for d in data:
            res[d] = self.search_one(text=d)
        return res

    def search_one(self, text: str, id=False) -> dict:
        """Search in ontology labels one by one.

        Args:
            text: search pattern
            id: whether to search by the id

        Returns:
            A list of ontology names
        """
        if id:
            text = text.replace(":", "_")
            res = self.onto.search(iri=f"*{text}")
        else:
            res = self.onto.search(label=text)

        return {i.name: i.label[0] for i in res}

    @format_into_dataframe
    def standardize(self, terms: pd.DataFrame, _reformat=False):
        """Checks if the ontology names are valid and in use.

        Args:
            terms: ontology ids

        Returns:
            a dataframe
        """
        terms.index = terms.index.str.replace(":", "_")
        terms.index.name = "ontology_id"
        terms["name"] = ""
        nonstd = {}
        for term in terms.index:
            # Ensuring the format of the IDs
            if term in self.onto_dict.keys():
                label = self.onto_dict[term]
                terms.loc[term]["name"] = label
                if label.startswith("obsolete"):
                    nonstd[term] = label
            else:
                nonstd[term] = label

        if len(nonstd) > 0:
            logg.warn(
                "The following terms were found to be obsolete or non-exist! Please"
                f" search the correct term via `.search`! \n {nonstd}"
            )

        if _reformat:
            return terms
