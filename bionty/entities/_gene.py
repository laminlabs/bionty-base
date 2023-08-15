from typing import Dict, Literal, Optional

import pandas as pd
from lamin_utils import logger

from .._bionty import Bionty
from ._shared_docstrings import _doc_params, doc_entites
from ._species import Species


@_doc_params(doc_entities=doc_entites)
class Gene(Bionty):
    """Gene.

    1. Ensembl
    Edits of terms are coordinated and reviewed on:
    https://www.ensembl.org/

    Args:
        {doc_entities}

    Notes:
        Biotypes: https://www.ensembl.org/info/genome/genebuild/biotypes.html
        Gene Naming: https://www.ensembl.org/info/genome/genebuild/gene_names.html
    """

    def __init__(
        self,
        species: str = "human",
        source: Optional[Literal["ensembl"]] = None,
        version: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            source=source,
            version=version,
            species=species,
            **kwargs,
        )


class EnsemblGene:
    def __init__(self, species: str, version: str) -> None:
        """Ensembl Gene mysql.

        Args:
            species: a bionty.Species object
            version: name of the ensembl DB version, e.g. "release-110"
        """
        self._import()
        self._species = (
            Species(version=version).lookup().dict().get(species)  # type:ignore
        )
        self._url = (
            f"mysql+mysqldb://anonymous:@ensembldb.ensembl.org/{self._species.core_db}"
        )

    def _import(self):
        try:
            import mysql.connector as sql  # noqa
            from sqlalchemy import create_engine  # noqa
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "To download Gene table from Ensembl, please run `pip install"
                " sqlalchemy,mysqlclient`"
            )

    def external_dbs(self):
        import mysql.connector as sql  # noqa
        from sqlalchemy import create_engine

        engine = create_engine(url=self._url)
        return pd.read_sql("SELECT * FROM external_db", con=engine)

    def download_df(self, external_db_names: Optional[Dict] = None) -> pd.DataFrame:
        """Fetch gene table from Ensembl mysql database.

        Args:
            external_db_names: {external database name : df column name}, see `.external_dbs()`
                Default is {"EntrezGene": "ensembl_gene_id"}.
        """
        import mysql.connector as sql  # noqa
        from sqlalchemy import create_engine

        query_core = """
        SELECT gene.stable_id, xref.display_label, gene.biotype, gene.description, external_synonym.synonym
        FROM gene
        LEFT JOIN xref ON gene.display_xref_id = xref.xref_id
        LEFT JOIN external_synonym ON gene.display_xref_id = external_synonym.xref_id
        """

        entrez_name = {"EntrezGene": "ensembl_gene_id"}
        if external_db_names is None:
            external_db_names = entrez_name
        if entrez_name not in list(external_db_names.keys()):
            external_db_names.update(entrez_name)
        external_db_names_str = ", ".join(
            [f"'{name}'" for name in external_db_names.keys()]
        )

        query_external = f"""
        SELECT gene.stable_id, object_xref.xref_id, xref.dbprimary_acc, external_db.db_name
        FROM gene
        LEFT JOIN object_xref ON gene.gene_id = object_xref.ensembl_id
        LEFT JOIN xref ON object_xref.xref_id = xref.xref_id
        LEFT JOIN external_db ON xref.external_db_id = external_db.external_db_id
        WHERE object_xref.ensembl_object_type = 'Gene' AND external_db.db_name IN ({external_db_names_str}) # noqa
        """

        engine = create_engine(url=self._url)

        # Query for the basic gene annotations:
        results_core = pd.read_sql(query_core, con=engine)
        logger.info("Fetching records from the core DB...")

        # aggregate metadata based on ensembl stable_id
        results_core_group = results_core.groupby("stable_id").agg(
            {
                "display_label": "first",
                "biotype": "first",
                "description": "first",
                "synonym": lambda x: "|".join([i for i in set(x) if i is not None]),
            }
        )

        # Query for external ids:
        results_external = pd.read_sql(query_external, con=engine)
        logger.info("Fetching records from the external DBs...")

        def add_external_db_column(df: pd.DataFrame, ext_db: str, df_col: str):
            # ncbi_gene_id
            ext = (
                results_external[results_external["db_name"] == ext_db]
                .drop_duplicates(["stable_id", "dbprimary_acc"])
                .drop(columns=["xref_id", "db_name"])
            )
            ext.rename(columns={"dbprimary_acc": df_col}, inplace=True)
            ext = ext.set_index("stable_id")
            dup = ext[ext.index.duplicated(keep=False)]
            if dup.shape[0] > 0:
                logger.warning(
                    f"Duplicated #rows ensembl_gene_id with {df_col}: {dup.shape[0]}"
                )
            df_merge = df.merge(ext, left_index=True, right_index=True, how="outer")
            return df_merge

        df = add_external_db_column(
            df=results_core_group, ext_db="EntrezGene", df_col="ncbi_gene_id"
        )

        for ext_db, df_col in external_db_names.items():
            if ext_db == "EntrezGene":
                continue
            df = add_external_db_column(df=df, ext_db=ext_db, df_col=df_col)

        df = df.reset_index()
        df.rename(
            columns={
                "stable_id": "ensembl_gene_id",
                "display_label": "symbol",
                "synonym": "synonyms",
            },
            inplace=True,
        )
        df_res = df.loc[
            :,
            [
                "ensembl_gene_id",
                "symbol",
                "ncbi_gene_id",
                "biotype",
                "description",
                "synonyms",
            ],
        ].copy()
        for col in df.columns:
            if col not in df_res.columns:
                df_res[col] = df[col]
        df_res = df_res[~df_res["ensembl_gene_id"].isnull()]
        df_res = df_res[~df_res["ensembl_gene_id"].isna()]

        # if stable_id is not ensembl_gene_id, keep a stable_id column
        if not any(df_res["ensembl_gene_id"].str.startswith("ENS")):
            logger.warning("No ensembl_gene_id found, writing to table_id column.")
            df_res.insert(0, "stable_id", df_res.pop("ensembl_gene_id"))
            df_res = df_res.sort_values("stable_id").reset_index(drop=True)
        else:
            df_res = df_res[df_res["ensembl_gene_id"].str.startswith("ENS")]
            df_res = df_res.sort_values("ensembl_gene_id").reset_index(drop=True)

        logger.success(f"Downloaded Gene table containing {df_res.shape[0]} entries.")

        return df_res
