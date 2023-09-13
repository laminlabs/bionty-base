import pandas as pd
import pytest

import bionty as bt


@pytest.fixture(scope="module")
def genes():
    data = {
        "gene symbol": ["A1CF", "A1BG", "FANCD1", "corrupted"],
        "ncbi id": ["29974", "1", "5133", "corrupted"],
        "ensembl_gene_id": [
            "ENSG00000148584",
            "ENSG00000121410",
            "ENSG00000188389",
            "ENSG0000corrupted",
        ],
    }
    df = pd.DataFrame(data).set_index("ensembl_gene_id")

    gn = bt.Gene(source="ensembl")

    return df, gn


def test_gene_ensembl_inspect_hgnc_id(genes):
    df, gn = genes

    inspected_df = gn.inspect(df["ncbi id"], field=gn.ncbi_gene_id, return_df=True)

    inspect = inspected_df["__validated__"].reset_index(drop=True)
    expected_series = pd.Series([True, True, True, False])

    assert inspect.equals(expected_series)


def test_ensemblgene_download():
    from bionty.entities._gene import EnsemblGene

    ensembl_gene = EnsemblGene(species="human", version="release-110")
    assert ensembl_gene._species.name == "human"

    external_df = ensembl_gene.external_dbs()
    assert external_df.shape[0] > 1

    df = ensembl_gene.download_df(external_db_names={"HGNC": "hgnc_id"})
    assert df.shape[0] > 6000
    assert "hgnc_id" in df.columns


def test_ensemblgene_map_legacy_ids():
    gn = bt.Gene(species="human", version="release-110")
    legacy_genes = [
        "ENSG00000280710",
        "ENSG00000261490",
        "ENSG00000203812",
        "ENSG00000204092",
        "ENSG00000215271",
    ]
    result = gn.map_legacy_ids(legacy_genes)
    assert result == {
        "mapped": {
            "ENSG00000204092": "ENSG00000226070",
            "ENSG00000215271": "ENSG00000290292",
            "ENSG00000261490": "ENSG00000071127",
            "ENSG00000280710": "ENSG00000125304",
        },
        "ambiguous": {"ENSG00000203812": ["ENSG00000288859", "ENSG00000288825"]},
        "unmapped": [],
    }

    result = gn.map_legacy_ids("ENSG00000280710")
    assert result == {
        "mapped": {"ENSG00000280710": "ENSG00000125304"},
        "ambiguous": {},
        "unmapped": [],
    }

    result = gn.map_legacy_ids(["ENSG00000280710"])
    assert result == {
        "mapped": {"ENSG00000280710": "ENSG00000125304"},
        "ambiguous": {},
        "unmapped": [],
    }
