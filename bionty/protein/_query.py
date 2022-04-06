from typing import Iterable, Optional
import io
import pandas as pd
import urllib.parse
import urllib.request
from ..species import Species


class Uniprot:
    """Wrapper of the Uniprot REST APIs

    See: https://www.uniprot.org/help/api_idmapping
    """

    _URL = "https://www.uniprot.org/uploadlists/"

    def __init__(self) -> None:
        pass

    def query(
        self,
        prots: Iterable[str],
        id_type_from="UNIPROT_ID",
        id_type_to="ENSEMBL_ID",
        columns: Optional[str] = None,
        species: Optional[str] = "human",
    ):

        # replace UNIPROT_ID with ACC
        colnames = (
            columns.split(",") + [id_type_from, id_type_to]
            if columns is not None
            else [id_type_from, id_type_to]
        )
        id_type_from = "ACC" if id_type_from == "UNIPROT_ID" else id_type_from
        id_type_to = "ACC" if id_type_to == "UNIPROT_ID" else id_type_to

        # taxon id of species
        taxon_id = Species(species=species).get_attribute("taxon_id")

        # set up params
        params = {
            "from": id_type_from,
            "to": id_type_to,
            "columns": columns,
            "format": "tab",
            "query": " ".join([i for i in prots]),
            "taxon": taxon_id,
        }

        # query uniprot
        data = urllib.parse.urlencode(params)
        data = data.encode("utf-8")
        req = urllib.request.Request(self._URL, data)
        with urllib.request.urlopen(req) as f:
            response = f.read()

        # format results into a dataframe
        data = response.decode("utf-8")
        df = pd.read_csv(io.StringIO(data), sep="\t", header=0)
        df.columns = colnames

        return df
