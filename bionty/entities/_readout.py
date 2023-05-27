from functools import cached_property
from typing import Literal, Optional

import pandas as pd
from lamin_logger import logger

from bionty.entities._shared_docstrings import _doc_params, species_removed

from .._entity import Bionty
from .._ontology import Ontology
from ..dev._io import s3_bionty_assets


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
        **kwargs,
    ) -> None:
        self._prefix = "http://www.ebi.ac.uk/efo/"
        self._readout_terms = {
            "assay": "OBI:0000070",
            "assay_by_molecule": "EFO:0002772",
            "assay_by_instrument": "EFO:0002773",
            "assay_by_sequencer": "EFO:0003740",
            "measurement": "EFO:0001444",
        }
        super().__init__(
            source=source,
            version=version,
            include_id_prefixes={"efo": ["EFO", "http://www.ebi.ac.uk/efo/"]},
            **kwargs,
        )

    @cached_property
    def ontology(self) -> Ontology:  # type:ignore
        """The Pronto Ontology object.

        See: https://pronto.readthedocs.io/en/stable/api/pronto.Ontology.html
        """
        self._download_ontology_file()
        return Ontology(handle=self._local_ontology_path, prefix=self._prefix)

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

    def df(self) -> pd.DataFrame:
        """Pandas DataFrame."""
        # Extra parsing steps for EFO ontology
        if self.source == "efo":
            # Download and sync from s3://bionty-assets
            s3_bionty_assets(
                filename=self._parquet_filename,
                assets_base_url="s3://bionty-assets",
                localpath=self._local_parquet_path,
            )
            # If download is not possible, write a parquet file from ontology
            if not self._local_parquet_path.exists():
                # write df to parquet file
                df = self._ontology_to_df(self.ontology).reset_index()
                # fix ontology_id before saving to parquet
                df["ontology_id"] = [
                    i.replace(self._prefix, "").replace("_", ":")
                    for i in df["ontology_id"]
                ]
                df["children"] = [
                    [j.replace(self._prefix, "").replace("_", ":") for j in i]
                    for i in df["children"]
                ]
                # parse terms
                logger.info("Parsing EFO terms for the first time will take 6-10min...")
                parsed_results = []
                for term in df["ontology_id"]:
                    parsed_results.append(self._parse(term))
                df_parsed = pd.DataFrame.from_records(parsed_results)
                df = df.merge(df_parsed).set_index("ontology_id")

                df.to_parquet(self._local_parquet_path)

            # loads the df and set index
            df = pd.read_parquet(self._local_parquet_path).reset_index()
            reference_index_name = self.reference_id
            if self.reference_id is None and "ontology_id" in df.columns:
                reference_index_name = "ontology_id"
            try:
                return df.set_index(reference_index_name)
            except KeyError:
                return df
        else:
            return super().df()

    def _parse(self, term_id: str) -> dict:
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
