from functools import cached_property
from pathlib import Path
from typing import Union

from owlready2 import get_ontology


class Ontology:
    """Ontology manager built on Owlready2.

    Args:
        base_iri: RDF/XML, OWL/XML or NTriples format
        load: Whether to load ontology
    """

    def __init__(self, base_iri: Union[str, Path], load: bool = True) -> None:
        if load:
            self._onto = get_ontology(base_iri).load()
        else:
            self._onto = get_ontology(base_iri)

    @property
    def onto(self):
        """owlready2 Ontology."""
        return self._onto

    @cached_property
    def onto_dict(self):
        """Dict of name:label."""
        return {i.name: i.label[0] for i in self.onto.classes()}

    def search(self, text: str, validate=False) -> dict:
        """Search in ontology labels.

        Args:
            text: search pattern
            validate: validation mode, checks if the ontology name exists and is in use

        Returns:
            A list of ontology names
        """
        if not validate:
            res = self.onto.search(label=text)
        else:
            res = self.onto.search(iri=f"*{text}")

        return {i.name: i.label[0] for i in res}
