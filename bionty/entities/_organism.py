from typing import Literal, Optional

import pandas as pd

from bionty.entities._shared_docstrings import _doc_params, organism_removed

from .._bionty import Bionty
from ..dev._io import s3_bionty_assets


@_doc_params(doc_entities=organism_removed)
class Organism(Bionty):
    """Organism.

    1. Organism ontology
    Edits of terms are coordinated and reviewed on:
    https://www.ensembl.org/index.html

    Args:
        {doc_entities}
    """

    def __init__(
        self,
        organism: Optional[
            Literal["vertebrates", "bacteria", "fungi", "metazoa", "plants", "all"]
        ] = None,
        source: Optional[Literal["ensembl", "ncbitaxon"]] = None,
        version: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(organism=organism, source=source, version=version, **kwargs)

    def _load_df(self) -> pd.DataFrame:
        if self.source == "ensembl":
            if not self._local_parquet_path.exists():
                # try to download from s3
                s3_bionty_assets(
                    filename=self._parquet_filename,
                    assets_base_url="s3://bionty-assets",
                    localpath=self._local_parquet_path,
                )

            # try to download from original url
            if not self._local_parquet_path.exists():
                self._url_download(self._url, self._local_ontology_path)  # type:ignore
                df = pd.read_csv(
                    self._local_ontology_path, sep="\t", index_col=False  # type:ignore
                )
                df.rename(
                    columns={
                        "#name": "name",
                        "species": "scientific_name",
                        "taxonomy_id": "ontology_id",
                    },
                    inplace=True,
                )
                df["name"] = df["name"].str.lower()
                df["ontology_id"] = "NCBITaxon:" + df["ontology_id"].astype(str)
                df.to_parquet(self._local_parquet_path)
                return df
            else:
                return pd.read_parquet(self._local_parquet_path)
        else:
            return super()._load_df()

    def df(self) -> pd.DataFrame:
        """Pandas DataFrame of the ontology.

        Returns:
            A Pandas DataFrame of the ontology.

        Examples:
            >>> import bionty as bt
            >>> bt.Organism().df()
        """
        return self._df.set_index("name")
