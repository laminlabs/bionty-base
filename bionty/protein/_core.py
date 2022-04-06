from typing import Iterable, Literal, Optional
import typing
from ..species import Species
from ._query import Uniprot

_IDs = Literal["UNIPROT_ID", "PDB_ID", "CHEMBL_ID", "DRUGBANK_ID", "ENSEMBL_PRO_ID"]


class Protein:
    """Protein"""

    def __init__(self, species="human"):
        self._species = Species(species=species)

    @property
    def species(self):
        """biomap.bioentity.Species"""
        return self._species

    @property
    def STD_ID(self):
        return "UNIPROT_ID"

    @property
    def attributes(self):
        return list(typing.get_args(_IDs))

    def get_attribute(
        self,
        prots: Iterable[str],
        id_type_from: Optional[_IDs],
        id_type_to: Optional[_IDs] = None,
    ):
        """Mapping between protein IDs

        Parameters
        ----------
        genes
            Input list
        id_type_from
            ID type of the input list, see `.attributes`
        id_type_to: str (Default is the `.STD_ID`)
            ID type to convert into

        Returns
        -------
        a dict of mapped ids
        """

        # default is to convert into STD_ID
        id_type_to = self.STD_ID if id_type_to is None else id_type_to

        # get mappings from the reference table
        res = Uniprot().query(
            prots,
            id_type_from=id_type_from,
            id_type_to=id_type_to,
            species=self.species.common_name,
        )
        df = res.reset_index().set_index(id_type_from)[[id_type_to]].copy()

        return df[df.index.isin(prots)].to_dict()[id_type_to]
