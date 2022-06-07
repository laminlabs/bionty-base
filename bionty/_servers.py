import xmltodict

from ._rest import fetch_endpoint
from ._urls import ENSEMBL_REST, ENSEMBL_REST_EXT


class EnsemblREST:
    """Queries via the Ensembl REST APIs."""

    def __init__(self) -> None:
        self._server = ENSEMBL_REST

    @property
    def server(self):
        """ENSEMBL_REST."""
        return self._server

    def species_info(self, return_raw=False):
        """ENSEMBL_REST_EXT.SPECIES_INFO."""
        ext = ENSEMBL_REST_EXT.SPECIES_INFO
        res = fetch_endpoint(self.server, ext, "text/xml")
        if return_raw:
            return res
        else:
            return xmltodict.parse(res)["opt"]["data"]["species"]
