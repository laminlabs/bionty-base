import re
from collections import namedtuple
from typing import Dict, Iterable, List, Tuple

import pandas as pd


class Lookup:
    """Lookup object with dot and [] access."""

    def __init__(
        self, df: pd.DataFrame, field: str, tuple_name="MyTuple", prefix: str = "bt"
    ) -> None:
        self._tuple_name = tuple_name
        lkeys = self._to_lookup_keys(values=df[field], prefix=prefix)
        self._df_dict = self._create_df_dict(df=df, field=field)
        self._lookup_dict = self._create_lookup_dict(lkeys=lkeys, df_dict=self._df_dict)

    def _to_lookup_keys(self, values: Iterable, prefix: str) -> Dict:
        """Convert a list of strings to tab-completion allowed formats.

        Returns:
            {lookup_key: value_or_values}
        """
        lkeys: Dict = {}
        for value in list(values):
            if not isinstance(value, str):
                continue
            # replace any special character with _
            lkey = re.sub("[^0-9a-zA-Z_]+", "_", str(value)).lower()
            if lkey == "":  # empty strings are skipped
                continue
            if not lkey[0].isalpha():  # must start with a letter
                lkey = f"{prefix.lower()}_{lkey}"

            if lkey in lkeys:
                # if multiple values have the same lookup key
                # put the values into a list
                self._append_records_to_list(df_dict=lkeys, value=lkey, record=value)
            else:
                lkeys[lkey] = value
        return lkeys

    def _create_df_dict(self, df: pd.DataFrame, field: str) -> Dict:
        """Create a dict with {lookup key: records in namedtuple}.

        Value is a list of namedtuples if multiple records match the same key.
        """
        df_dict: Dict = {}  # a dict of namedtuples as records and values as keys
        for i, row in enumerate(df.itertuples(index=False, name=self._tuple_name)):
            value = df[field][i]
            if not isinstance(value, str):
                continue
            if value in df_dict:
                self._append_records_to_list(df_dict=df_dict, value=value, record=row)
            else:
                df_dict[value] = row
        return df_dict

    def _append_records_to_list(self, df_dict: dict, value: str, record) -> None:
        """Append unique records to a list."""
        values_list = df_dict[value]
        if not isinstance(values_list, list):
            values_list = [values_list]
        values_set = set(values_list)
        values_set.add(record)
        df_dict[value] = list(values_set)

    def _create_lookup_dict(self, lkeys: dict, df_dict: dict) -> Dict:
        lkey_dict: Dict = {}  # a dict of namedtuples as records and lookup keys as keys
        for lkey, values in lkeys.items():
            if isinstance(values, list):
                combined_list = []
                for v in values:
                    records = df_dict.get(v)
                    if isinstance(records, list):
                        combined_list += records
                    else:
                        combined_list.append(records)
                lkey_dict[lkey] = combined_list
            else:
                lkey_dict[lkey] = df_dict.get(values)

        return lkey_dict

    def dict(self) -> Dict:
        """Dictionary of the lookup."""
        return self._df_dict

    def lookup(self) -> Tuple:
        """Lookup records with dot access."""
        keys: List = list(self._lookup_dict.keys()) + ["dict"]
        MyTuple = namedtuple("Lookup", keys)  # type:ignore
        return MyTuple(**self._lookup_dict, dict=self.dict)  # type:ignore
