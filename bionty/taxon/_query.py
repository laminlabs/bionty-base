from biothings_client import MyTaxonInfo


class Mytaxon(MyTaxonInfo):
    """Wrapper of MyTaxon.info"""

    def __init__(self) -> None:
        super().__init__()
