import typing
from typing import Iterable, Literal, Optional

from ..species import Species as SP
from ._query import Uniprot

_IDs = Literal["UNIPROT_ID", "PDB_ID", "CHEMBL_ID", "DRUGBANK_ID", "ENSEMBL_PRO_ID"]


class Protein:
    """Protein."""

    def __init__(self, species="human"):
        self._species = SP(common_name=species)

    @property
    def species(self):
        """bionty.species()."""
        return self._species

    @property
    def std_id(self):
        """Standardized id."""
        return "UNIPROT_ID"

    @property
    def fields(self):
        """List all protein related fields."""
        return list(typing.get_args(_IDs))

    def search(
        self,
        prots: Iterable[str],
        id_type_from: Optional[_IDs],
        id_type_to: Optional[_IDs] = None,
    ):
        """Mapping between protein IDs.

        Args:
            prots: Input list
            id_type_from: ID type of the input list, see `.fields`
            id_type_to: ID type to convert into
                Default is the `.std_id`

        Returns:
            a dict of mapped ids
        """
        # default is to convert into std_id
        id_type_to = self.std_id if id_type_to is None else id_type_to

        # get mappings from the reference table
        res = Uniprot().query(
            prots,
            id_type_from=id_type_from,
            id_type_to=id_type_to,
            species=self.species.std_name,
        )
        df = res.reset_index().set_index(id_type_from)[[id_type_to]].copy()

        return df[df.index.isin(prots)].to_dict()[id_type_to]
