import pandas as pd

from .._servers import EnsemblREST
from .main import SPECIES_FILENAME

SPECIES_COLS = [
    "scientific_name",
    "display_name",
    "common_name",
    "taxon_id",
    "assembly",
    "accession",
    "release",
]


def update_species_table() -> None:
    """Fetch species table from Ensembl REST.

    Returns:
        a dataframe
    """
    entries = EnsemblREST().species_info()

    # format into a dataframe
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
