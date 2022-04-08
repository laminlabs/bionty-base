from biothings_client import get_client


class Mytaxon(get_client("taxon", instance=False)):
    """Wrapper of MyTaxon.info"""

    def __init__(self) -> None:
        super().__init__()
