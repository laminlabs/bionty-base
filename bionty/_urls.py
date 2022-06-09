from argparse import Namespace

# Ensembl REST server
ENSEMBL_REST = "http://rest.ensembl.org"
ENSEMBL_REST_EXT = Namespace(
    **{
        "SPECIES_INFO": "/info/species?",  # all species info
        "ARCHIVE_IDS": "/archive/id",  # retrieves the latest version of ids
        "XREFS_ID": "/xrefs/id/",
        "LOOKUP_IDS": "/lookup/id",
        "LOOKUP_SYMBOLS": "/lookup/symbol/",
        "SEQ_IDS": "/sequence/id",
    }
)

# HGNC REST server
"""See searchable fields here: https://www.genenames.org/help/rest/"""
HGNC_REST = "http://rest.genenames.org/"
HGNC_REST_EXT = Namespace(INFO="info", FETCH="fetch/", SEARCH="search/")

# The Open Biological and Biomedical Ontology (OBO) Foundry
"""Website: https://obofoundry.org/"""
OBO = "http://purl.obolibrary.org/obo/"
OBO_CL = OBO + "cl/cl-simple.obo"
OBO_CL_OWL = OBO + "cl/cl-simple.owl"
OBO_MONDO_OWL = OBO + "mondo/mondo-base.owl"
OBO_UBERON_OWL = OBO + "uberon/uberon-base.owl"
