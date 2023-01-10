from typing import Optional

import pandas as pd
from cached_property import cached_property

from .._ontology import Ontology
from .._settings import check_datasetdir_exists, settings
from .._table import EntityTable

EFO_DF_D3 = "https://bionty-assets.s3.amazonaws.com/efo_df.json"


class Readout(EntityTable):
    """Experimental Factor Ontology.

    https://www.ebi.ac.uk/ols/ontologies/efo

    Also see: `bionty.EntityTable <https://lamin.ai/docs/bionty/bionty.entitytable>`__
    """

    def __init__(
        self,
        id: str = "ontology_id",
        database: Optional[str] = None,
        version: Optional[str] = None,
    ) -> None:
        super().__init__(id=id, database=database, version=version)
        database = "efo" if database is None else database
        self._filepath = settings.datasetdir / "efo_df.json"
        self._readout_terms = {
            "assay": "OBI:0000070",
            "assay_by_molecule": "EFO:0002772",
            "assay_by_instrument": "EFO:0002773",
            "assay_by_sequencer": "EFO:0003740",
            "measurement": "EFO:0001444",
        }

    @cached_property
    def df(self) -> pd.DataFrame:
        """DataFrame."""
        if not self._filepath.exists():
            self._download_df()
        df = pd.read_json(self._filepath)
        df.index.name = "ontology_id"
        return df

    @cached_property
    def ontology(self) -> Ontology:  # type:ignore
        """EFO."""
        return super().ontology(prefix="http://www.ebi.ac.uk/efo/")

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
