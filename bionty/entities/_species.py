from typing import Literal, Optional

import pandas as pd

from bionty.entities._shared_docstrings import _doc_params, species_removed

from .._bionty import Bionty


@_doc_params(doc_entities=species_removed)
class Species(Bionty):
    """Species.

    1. Species ontology
    Edits of terms are coordinated and reviewed on:
    https://www.ensembl.org/index.html

    Args:
        {doc_entities}
    """

    def __init__(
        self,
        source: Optional[Literal["ensembl"]] = None,
        version: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(source=source, version=version, **kwargs)

    def _load_df(self) -> pd.DataFrame:
        if not self._local_parquet_path.exists():
            self._url_download(self._url, self._local_ontology_path)
            df = pd.read_csv(self._local_ontology_path, sep="\t", index_col=False)
            df.rename(
                columns={
                    "#name": "name",
                    "species": "scientific_name",
                    "taxonomy_id": "taxon_id",
                },
                inplace=True,
            )
            df["name"] = df["name"].str.lower()
            df.insert(0, "id", "NCBI_" + df["taxon_id"].astype(str))
            df.to_parquet(self._local_parquet_path)
            return df
        else:
            return pd.read_parquet(self._local_parquet_path)

    def df(self) -> pd.DataFrame:
        """Pandas DataFrame of the ontology.

        Returns:
            A Pandas DataFrame of the ontology.

        Examples:
            >>> import bionty as bt
            >>> bt.Species().df()
        """
        return self._df.set_index("name")
