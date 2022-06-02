from functools import cached_property
from pathlib import Path
from typing import Union

import pandas as pd

from ._settings import format_into_dataframe


class Ontology:
    """Ontology manager built on Owlready2.

    Args:
        base_iri: RDF/XML, OWL/XML or NTriples format
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
        """owlready2 Ontology."""
        return self._onto

    @cached_property
    def onto_dict(self) -> dict:
        """Dict of name:label."""
        return {i.name: i.label[0] for i in self.onto.classes()}

    @cached_property
    def classes(self) -> dict:
        """Indexed classes, owlready2 ThingClass object."""
        return {i.name: i for i in self.onto.classes()}

    def search(self, text: str) -> dict:
        """Search in ontology labels.

        Args:
            text: search pattern

        Returns:
            A list of ontology names
        """
        res = self.onto.search(label=text)

        return {i.name: i.label[0] for i in res}

    @format_into_dataframe
    def validate(self, terms: pd.DataFrame) -> None:
        """Checks if the ontology names exist and is in use.

        Args:
            terms: ontology ids
        """
        res = {}
        for term in terms.index:
            res[term] = self.onto.search(iri=f"*{term}")
