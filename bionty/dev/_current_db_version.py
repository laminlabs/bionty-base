import pandas as pd


def current_db_version(db: str):
    """Lookup the current version of a database."""
    db = db.lower()

    if db == "ensembl":
        # For Ensembl, parse the current_README file
        lines = []

        for line in pd.read_csv(
            "https://ftp.ensembl.org/pub/README",
            chunksize=1,
            header=None,
            encoding="utf-8",
        ):
            lines.append(line.iloc[0, 0])
        return "-".join(lines[1].split(" ")[1:-1]).lower()

    else:
        raise NotImplementedError
