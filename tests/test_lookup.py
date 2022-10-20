from bionty import lookup


def test_lookup():
    assert lookup.gene_id.ensembl_gene_id == "ensembl_gene_id"
    assert lookup.protein_id.uniprotkb_id == "uniprotkb_id"
    assert lookup.species.mouse == "mouse"
