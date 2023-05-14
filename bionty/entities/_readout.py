from functools import cached_property
from typing import Literal, Optional

import pandas as pd

from bionty.entities._shared_docstrings import _doc_params, species_removed

from .._entity import Bionty
from .._ontology import Ontology
from .._settings import check_datasetdir_exists, settings

EFO_DF_D3 = "https://bionty-assets.s3.amazonaws.com/efo_df.json"


@_doc_params(doc_entities=species_removed)
class Readout(Bionty):
    """Experimental Factor.

    1. Experimental Factor Ontology
    Edits of terms are coordinated and reviewed on:
    https://www.ebi.ac.uk/ols/ontologies/efo

    Args:
        {doc_entities}

    Also see: `bionty.Bionty <https://lamin.ai/docs/bionty/bionty.entity>`__
    """

    def __init__(
        self,
        source: Optional[Literal["efo"]] = None,
        version: Optional[str] = None,
        **kwargs
    ) -> None:
        self._filepath = settings.datasetdir / "efo_df.json"
        super().__init__(
            source=source, version=version, reference_id="ontology_id", **kwargs
        )
        self._readout_terms = {
            "assay": "OBI:0000070",
            "assay_by_molecule": "EFO:0002772",
            "assay_by_instrument": "EFO:0002773",
            "assay_by_sequencer": "EFO:0003740",
            "measurement": "EFO:0001444",
        }

    @cached_property
    def ontology(self) -> Ontology:  # type:ignore
        """EFO."""
        localpath = self._url_download(self._url)

        return Ontology(handle=localpath, prefix="http://www.ebi.ac.uk/efo/")

    @cached_property
    def assay(self) -> list:
        """Assays."""
        # OBI:0000070
        return self.ontology._list_subclasses(self._readout_terms["assay"])

    @cached_property
    def assay_by_molecule(self) -> list:
        """Assays by molecule."""
        # EFO:0002772
        return self.ontology._list_subclasses(self._readout_terms["assay_by_molecule"])

    @cached_property
    def assay_by_instrument(self) -> list:
        """Assays by instrument."""
        # EFO:0002773
        return self.ontology._list_subclasses(
            self._readout_terms["assay_by_instrument"]
        )

    @cached_property
    def assay_by_sequencer(self) -> list:
        """Assay by sequencer."""
        # EFO:0003740
        return self.ontology._list_subclasses(self._readout_terms["assay_by_sequencer"])

    @cached_property
    def measurement(self) -> list:
        """Measurement."""
        # EFO:0001444
        return self.ontology._list_subclasses(self._readout_terms["measurement"])

    @check_datasetdir_exists
    def _download_df(self) -> None:
        from urllib.request import urlretrieve

        urlretrieve(
            EFO_DF_D3,
            self._filepath,
        )

    def df(self) -> pd.DataFrame:
        """DataFrame."""
        if not self._filepath.exists():
            self._download_df()
        df = pd.read_json(self._filepath)
        df.index.name = "ontology_id"
        df = df.reset_index()

        return df

    def get(self, term_id: str) -> dict:
        """Parse readout attributes from EFO."""

        def _list_to_str(lst: list):
            if len(lst) == 0:
                return None
            elif len(lst) == 1:
                return lst[0].name  # type: ignore
            else:
                return ";".join([i.name for i in lst])

        term = self.ontology.get_term(term_id)
        superclasses = term.superclasses()

        # get the molecule term
        molecules = [i for i in self.assay_by_molecule if i in superclasses]
        # get the instrument term
        instruments = [i for i in self.assay_by_sequencer if i in superclasses]
        if len(instruments) == 0:
            instruments = [i for i in self.assay_by_instrument if i in superclasses]
        # get the measurement for non-molecular readouts
        measurements = [i for i in self.measurement if i in superclasses]

        readout = {
            "ontology_id": term_id,
            "name": term.name,
            "molecule": _list_to_str(molecules),
            "instrument": _list_to_str(instruments),
            "measurement": _list_to_str(measurements),
        }

        return readout
