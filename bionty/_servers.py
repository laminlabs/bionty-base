import xmltodict

from ._httpx import get_request, get_request_async, post_request
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
        res = get_request(self.server, ext, "text/xml")
        if return_raw:
            return res
        else:
            return xmltodict.parse(res)["opt"]["data"]["species"]

    def xref(self, ids, **kwargs):
        """Retrieve external references of Ensembl ids.

        See https://rest.ensembl.org/documentation/info/xref_id
        """
        if isinstance(ids, str):
            ext = f"{ENSEMBL_REST_EXT.XREFS_ID}{ids}?"
            res = get_request(self.server, ext, **kwargs)
        else:
            res = get_request_async(self.server + ENSEMBL_REST_EXT.XREFS_ID, ids)
        return res

    def archive_ids(self, ids):
        """Retrieve the latest version for a set of identifiers."""
        ext = ENSEMBL_REST_EXT.ARCHIVE_IDS
        res = post_request(self.server, ext, data=self._config_data(ids, "id"))
        return res

    def lookup_ids(self, ids, **kwargs):
        """Find the species and database for several identifiers.

        See https://rest.ensembl.org/documentation/info/lookup_post
        """
        ext = ENSEMBL_REST_EXT.LOOKUP_IDS
        res = post_request(
            self.server, ext, data=self._config_data(ids, "id"), **kwargs
        )
        return res

    def lookup_symbols(self, symbols, species="homo_sapiens", **kwargs):
        """Find the species and database for symbols in a linked external database."""
        ext = f"{ENSEMBL_REST_EXT.LOOKUP_SYMBOLS}{species}"
        res = post_request(self.server, ext, data=self._config_data(symbols), **kwargs)
        return res

    def seq_ids(self, ids, **kwargs):
        """Request multiple types of sequence by a stable identifier list."""
        ext = ENSEMBL_REST_EXT.SEQ_IDS
        res = post_request(self.server, ext, data=self._config_data(ids), **kwargs)
        return res
