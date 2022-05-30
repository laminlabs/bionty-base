from argparse import Namespace

# Ensembl REST server
ENSEMBL_REST = "http://rest.ensembl.org/"
ENSEMBL_REST_EXT = Namespace(SPECIES_INFO="info/species?")

# HGNC REST server
"""See searchable fields here: https://www.genenames.org/help/rest/"""
HGNC_REST = "http://rest.genenames.org/"
HGNC_REST_EXT = Namespace(INFO="info", FETCH="fetch/", SEARCH="search/")
