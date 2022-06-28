import pandas as pd


class Table:
    """Biological entity as a table.

    See :doc:`tutorial/index` for background.
    """

    @cached_property
    def df(self) -> pd.DataFrame:
        """DataFrame."""
        raise NotImplementedError
