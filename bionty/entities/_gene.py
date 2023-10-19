from typing import Dict, Iterable, Literal, Optional

import pandas as pd
from lamin_utils import logger

from .._bionty import Bionty
from .._settings import settings
from ..dev._io import s3_bionty_assets
from ._organism import Organism
from ._shared_docstrings import _doc_params, doc_entites


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
        organism: str = "human",
        source: Optional[Literal["ensembl"]] = None,
        version: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(
            source=source,
            version=version,
            organism=organism,
            **kwargs,
        )

    def map_legacy_ids(self, values: Iterable):
        """Convert legacy ids to current ids."""
        if self.source != "ensembl":
            raise NotImplementedError
        if isinstance(values, str):
            values = [values]
        ensembl = EnsemblGene(organism=self.organism, version=self.version)
        legacy_df_filename = f"df-legacy_{self.organism}__{self.source}__{self.version}__{self.__class__.__name__}.parquet"  # noqa
        legacy_df_localpath = settings.dynamicdir / legacy_df_filename
        s3_bionty_assets(
            filename=legacy_df_filename,
            assets_base_url="s3://bionty-assets",
            localpath=legacy_df_localpath,
        )
        try:
            results = pd.read_parquet(legacy_df_localpath)
        except FileNotFoundError:
            raise NotImplementedError
        results = results[results.old_stable_id.isin(values)].copy()
        return ensembl._process_convert_result(results, values=values)


class EnsemblGene:
    def __init__(self, organism: str, version: str) -> None:
        """Ensembl Gene mysql.

        Args:
            organism: a bionty.Organism object
            version: name of the ensembl DB version, e.g. "release-110"
        """
        self._import()
        import mysql.connector as sql  # noqa
        from sqlalchemy import create_engine

        self._organism = (
            Organism(version=version).lookup().dict().get(organism)  # type:ignore
        )
        self._url = (
            f"mysql+mysqldb://anonymous:@ensembldb.ensembl.org/{self._organism.core_db}"
        )
        self._engine = create_engine(url=self._url)

    def _import(self):
        try:
            import mysql.connector as sql  # noqa
            from sqlalchemy import create_engine  # noqa
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "To query from the Ensembl database, please run `pip install"
                " sqlalchemy,mysqlclient`"
            )

    def external_dbs(self):
        return pd.read_sql("SELECT * FROM external_db", con=self._engine)

    def download_df(self, external_db_names: Optional[Dict] = None) -> pd.DataFrame:
        """Fetch gene table from Ensembl mysql database.

        Args:
            external_db_names: {external database name : df column name}, see `.external_dbs()`
                Default is {"EntrezGene": "ensembl_gene_id"}.
        """
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

        # Query for the basic gene annotations:
        results_core = pd.read_sql(query_core, con=self._engine)
        logger.info("fetching records from the core DB...")

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
        results_external = pd.read_sql(query_external, con=self._engine)
        logger.info("fetching records from the external DBs...")

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
                    f"duplicated #rows ensembl_gene_id with {df_col}: {dup.shape[0]}"
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
            logger.warning("no ensembl_gene_id found, writing to table_id column.")
            df_res.insert(0, "stable_id", df_res.pop("ensembl_gene_id"))
            df_res = df_res.sort_values("stable_id").reset_index(drop=True)
        else:
            df_res = df_res[df_res["ensembl_gene_id"].str.startswith("ENS")]
            df_res = df_res.sort_values("ensembl_gene_id").reset_index(drop=True)

        logger.success(f"downloaded Gene table containing {df_res.shape[0]} entries.")

        return df_res

    def download_legacy_ids_df(self, df: pd.DataFrame, col: Optional[str] = None):
        col = "ensembl_gene_id" if col is None else col
        current_ids = tuple(df[col])
        results = pd.read_sql(
            "SELECT * FROM stable_id_event JOIN mapping_session USING"
            " (mapping_session_id) WHERE type = 'gene' AND new_stable_id IN"
            f" {current_ids} AND score > 0 AND old_stable_id != new_stable_id",  # noqa
            con=self._engine,
        )
        return results

    def _process_convert_result(
        self,
        results: pd.DataFrame,
        values: Iterable,
    ):
        # unique mappings
        mapper = (
            results.drop_duplicates(["old_stable_id"], keep=False)
            .set_index("old_stable_id")["new_stable_id"]
            .to_dict()
        )
        # ambiguous mappings
        ambiguous = (
            results[~results["old_stable_id"].isin(mapper)][
                ["old_stable_id", "new_stable_id"]
            ]
            .groupby("old_stable_id", group_keys=False)["new_stable_id"]
            .apply(list)
            .to_dict()
        )
        # unmappables
        unmapped = set(values).difference(results["old_stable_id"])
        return {"mapped": mapper, "ambiguous": ambiguous, "unmapped": list(unmapped)}

    def map_legacy_ids(self, values: Iterable, df: pd.DataFrame):
        if isinstance(values, str):
            legacy_genes = f"('{values}')"
            values = [values]
        else:
            legacy_genes = tuple(values)  # type:ignore
        if len(legacy_genes) == 1:
            legacy_genes = f"('{legacy_genes[0]}')"

        current_ids = tuple(df.ensembl_gene_id)
        # query the ensembl mysql db
        results = pd.read_sql(
            "SELECT * FROM stable_id_event JOIN mapping_session USING"
            " (mapping_session_id) WHERE type = 'gene' AND old_stable_id IN"
            f" {legacy_genes} AND new_stable_id IN {current_ids} AND old_stable_id !="
            " new_stable_id",  # noqa
            con=self._engine,
        )
        return self._process_convert_result(results, values)
