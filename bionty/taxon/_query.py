import sys
from pathlib import Path

import pandas as pd
import requests  # type: ignore
import xmltodict

from .._urls import ENSEMBL_REST, ENSEMBL_REST_EXT
from ._core import SPECIES_COLS

HERE = Path(__file__).parent
SPECIES_FILENAME = HERE / "tables/Species.csv"


def update_species_table() -> None:
    """Fetch species table from Ensembl REST.

    Returns:
        a dataframe
    """
    server = ENSEMBL_REST
    ext = ENSEMBL_REST_EXT.SPECIES_INFO

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
        for i in SPECIES_COLS:
            if i != "scientific_name":
                sp_dict[id].append(entry.get(f"@{i}"))
    sp_df = pd.DataFrame.from_dict(sp_dict).T
    sp_df.columns = cols
    sp_df.index.name = "scientific_name"
    sp_df["display_name"] = sp_df["display_name"].str.lower()
    # Adding a short_name column
    sp_df["short_name"] = [f'{i[0].lower()}{i.split("_")[-1]}' for i in sp_df.index]
    # Set display_name as the index for std_id
    sp_df = sp_df.reset_index().set_index("display_name")
    sp_df.to_csv(SPECIES_FILENAME, header=True, index=True)


class Mytaxon:
    """Wrapper of MyTaxon.info."""

    def __init__(self) -> None:
        from biothings_client import get_client

        self.sever = get_client("taxon", instance=False)
