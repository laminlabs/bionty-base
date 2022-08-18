from bionty import lookup


def test_lookup():
    assert lookup.gene_id.ensembl_gene_id == "ensembl_gene_id"
    assert lookup.feature_model.gene == "gene"
    assert lookup.species.mouse == "mouse"
    assert lookup.cell_type.CL_0000057 == "CL:0000057"
    assert lookup.disease.MONDO_0000006 == "MONDO_0000006"
