from argparse import Namespace

# Ensembl REST server


# HGNC REST server
"""See searchable fields here: https://www.genenames.org/help/rest/"""
HGNC_REST = "http://rest.genenames.org/"
HGNC_REST_EXT = Namespace(INFO="info", FETCH="fetch/", SEARCH="search/")

# The Open Biological and Biomedical Ontology (OBO) Foundry
"""Website: https://obofoundry.org/"""
OBO = "http://purl.obolibrary.org/obo/"
OBO_UBERON_OWL = OBO + "uberon/uberon-base.owl"
