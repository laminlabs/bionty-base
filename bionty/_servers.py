import xmltodict

from ._rest import fetch_endpoint, fetch_endpoint_POST
from ._urls import ENSEMBL_REST, ENSEMBL_REST_EXT


class EnsemblREST:
    """Queries via the Ensembl REST APIs."""

    def __init__(self) -> None:
        self._server = ENSEMBL_REST

    @property
    def server(self):
        """ENSEMBL_REST."""
        return self._server

    def _config_data(self, ids, label):
        ids = str(ids).replace("'", '"')
        return f'{{ "{label}" : {ids} }}'

    def species_info(self, return_raw=False):
        """ENSEMBL_REST_EXT.SPECIES_INFO."""
        ext = ENSEMBL_REST_EXT.SPECIES_INFO
        res = fetch_endpoint(self.server, ext, "text/xml")
        if return_raw:
            return res
        else:
            return xmltodict.parse(res)["opt"]["data"]["species"]

    def xref(self, id, **kwds):
        """Retrieve external references if an Ensembl id.

        See https://rest.ensembl.org/documentation/info/xref_id
        """
        ext = f"{ENSEMBL_REST_EXT.XREFS_ID}{id}?"
        res = fetch_endpoint(self.server, ext, **kwds)
        return res

    def archive_ids(self, ids):
        """Retrieve the latest version for a set of identifiers."""
        ext = ENSEMBL_REST_EXT.ARCHIVE_IDS
        res = fetch_endpoint_POST(self.server, ext, data=self._config_data(ids, "id"))
        return res

    def lookup_ids(self, ids, **kwds):
        """Find the species and database for several identifiers.

        See https://rest.ensembl.org/documentation/info/lookup_post
        """
        ext = ENSEMBL_REST_EXT.LOOKUP_IDS
        res = fetch_endpoint_POST(
            self.server, ext, data=self._config_data(ids, "id"), **kwds
        )
        return res

    def lookup_symbols(self, symbols, species="homo_sapiens", **kwds):
        """Find the species and database for symbols in a linked external database."""
        ext = f"{ENSEMBL_REST_EXT.LOOKUP_SYMBOLS}{species}"
        res = fetch_endpoint_POST(
            self.server, ext, data=self._config_data(symbols), **kwds
        )
        return res

    def seq_ids(self, ids, **kwds):
        """Request multiple types of sequence by a stable identifier list."""
        ext = ENSEMBL_REST_EXT.SEQ_IDS
        res = fetch_endpoint_POST(self.server, ext, data=self._config_data(ids), **kwds)
        return res
