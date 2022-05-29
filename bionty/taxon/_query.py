import sys

import pandas as pd
import requests  # type: ignore
import xmltodict

from .._urls import ENSEMBL_REST, ENSEMBL_REST_EXT


class Mytaxon:
    """Wrapper of MyTaxon.info."""

    def __init__(self) -> None:
        from biothings_client import get_client

        self.sever = get_client("taxon", instance=False)


def species_table() -> pd.DataFrame:
    """Fetch species table from Ensembl REST.

    Returns:
        a dataframe
    """
    server = ENSEMBL_REST
    ext = ENSEMBL_REST_EXT.SPECIES_INO

    r = requests.get(server + ext, headers={"Content-Type": "text/xml"})
    if not r.ok:
        r.raise_for_status()
        sys.exit()

    # format into a dataframe
    entries = xmltodict.parse(r.text)["opt"]["data"]["species"]
    sp_dict: dict = {}
    cols = [
        "display_name",
        "common_name",
        "taxon_id",
        "assembly",
        "accession",
        "release",
    ]
    for entry in entries:
        id = entry.get("@name")
        sp_dict[id] = []
        for i in cols:
            sp_dict[id].append(entry.get(f"@{i}"))
    sp_df = pd.DataFrame.from_dict(sp_dict).T
    sp_df.columns = cols

    return sp_df
