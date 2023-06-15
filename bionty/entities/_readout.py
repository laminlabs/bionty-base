from functools import cached_property
from typing import Literal, Optional

import pandas as pd
from lamin_logger import logger

from bionty.entities._shared_docstrings import _doc_params, species_removed

from .._bionty import Bionty
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
        self._download_ontology_file(
            localpath=self._local_ontology_path,  # type:ignore
            url=self._url,
            md5=self._md5,
        )
        return Ontology(handle=self._local_ontology_path, prefix=self._prefix)

    def _load_df(self) -> pd.DataFrame:
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
                df = self.ontology.to_df(
                    source=self.source, include_id_prefixes=self.include_id_prefixes
                ).reset_index()
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
            return pd.read_parquet(self._local_parquet_path)
        else:
            return super()._load_df()

    def _parse(self, term_id: str) -> dict:
        """Parse readout attributes from EFO."""

        def _list_to_str(lst: list):
            if len(lst) == 0:
                return None
            elif len(lst) == 1:
                return lst[0].name  # type: ignore
            else:
                return ";".join([i.name for i in lst])

        def _list_subclasses(ontology: Ontology, term, *, distance=1, with_self=False):
            """Subclasses of a term."""
            termclass = ontology.get_term(term)
            return list(termclass.subclasses(distance=distance, with_self=with_self))

        term = self.ontology.get_term(term_id)
        superclasses = term.superclasses()

        # assay = self.ontology._list_subclasses(self._readout_terms["assay"])
        assay_by_molecule = _list_subclasses(
            self.ontology, self._readout_terms["assay_by_molecule"]
        )
        assay_by_instrument = _list_subclasses(
            self.ontology, self._readout_terms["assay_by_instrument"]
        )

        assay_by_sequencer = _list_subclasses(
            self.ontology, self._readout_terms["assay_by_sequencer"]
        )
        measurement = _list_subclasses(
            self.ontology, self._readout_terms["measurement"]
        )

        # get the molecule term
        molecules = [i for i in assay_by_molecule if i in superclasses]
        # get the instrument term
        instruments = [i for i in assay_by_sequencer if i in superclasses]
        if len(instruments) == 0:
            instruments = [i for i in assay_by_instrument if i in superclasses]
        # get the measurement for non-molecular readouts
        measurements = [i for i in measurement if i in superclasses]

        readout = {
            "ontology_id": term_id,
            "name": term.name,
            "molecule": _list_to_str(molecules),
            "instrument": _list_to_str(instruments),
            "measurement": _list_to_str(measurements),
        }

        return readout
