from biothings_client import get_client


class Mytaxon:
    """Wrapper of MyTaxon.info."""

    def __init__(self) -> None:
        self.sever = get_client("taxon", instance=False)
