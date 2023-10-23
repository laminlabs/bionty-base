from functools import cached_property
from typing import Dict, Literal, Optional

import pandas as pd
from lamin_utils import logger

from bionty.entities._shared_docstrings import _doc_params, organism_removed

from .._bionty import Bionty
from .._ontology import Ontology


@_doc_params(doc_entities=organism_removed)
class ExperimentalFactor(Bionty):
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
        organism: Optional[Literal["all"]] = None,
        source: Optional[Literal["efo"]] = None,
        version: Optional[str] = None,
        **kwargs,
    ) -> None:
        super().__init__(
            organism=organism,
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
            url=self._url,  # type:ignore
            md5=self._md5,  # type:ignore
        )
        onto = Ontology(
            handle=self._local_ontology_path,  # type:ignore
            prefix="http://www.ebi.ac.uk/efo/",
        )
        # TODO: fix
        onto.__setattr__("efo_to_df", efo_to_df)
        return onto


def _parse_efo_term(
    term_id: str,
    ontology: Ontology,
) -> Dict:
    """Parse readout attributes from EFO."""
    readout_terms = {
        "assay": "OBI:0000070",
        "assay_by_molecule": "EFO:0002772",
        "assay_by_instrument": "EFO:0002773",
        "assay_by_sequencer": "EFO:0003740",
        "measurement": "EFO:0001444",
    }

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

    term = ontology.get_term(term_id)
    superclasses = term.superclasses()

    # assay = _list_subclasses(readout_terms["assay"])
    assay_by_molecule = _list_subclasses(ontology, readout_terms["assay_by_molecule"])
    assay_by_instrument = _list_subclasses(
        ontology, readout_terms["assay_by_instrument"]
    )

    assay_by_sequencer = _list_subclasses(ontology, readout_terms["assay_by_sequencer"])
    measurement = _list_subclasses(ontology, readout_terms["measurement"])

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


def efo_to_df(
    ontology: Ontology,
    source: str,
    include_id_prefixes: dict,
    prefix: str = "http://www.ebi.ac.uk/efo/",
) -> pd.DataFrame:  # pragma: no cover
    df = ontology.to_df(
        source=source, include_id_prefixes=include_id_prefixes
    ).reset_index()
    # fix ontology_id before saving to parquet
    df["ontology_id"] = [
        i.replace(prefix, "").replace("_", ":") for i in df["ontology_id"]
    ]
    df["parents"] = [
        [j.replace(prefix, "").replace("_", ":") for j in i] for i in df["parents"]
    ]
    # parse terms
    logger.info("parsing EFO terms for the first time will take 6-10min...")
    parsed_results = []
    for term in df["ontology_id"]:
        parsed_results.append(_parse_efo_term(term, ontology))
    df_parsed = pd.DataFrame.from_records(parsed_results)
    df = df.merge(df_parsed).set_index("ontology_id")

    return df
