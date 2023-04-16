import json
from collections import namedtuple
from typing import Iterable
from urllib.request import urlretrieve

from ._normalize import GENE_COLUMNS, PROTEIN_COLUMNS


def _lookup(values: Iterable[str]):
    """Look up a list of values via tab completion."""
    nt = namedtuple("feature", values)  # type: ignore
    return nt(**{i: i for i in values})


class lookup:
    """Look up a list of values via tab completion."""

    gene_id = _lookup(values=set(GENE_COLUMNS.values()))
    protein_id = _lookup(values=set(PROTEIN_COLUMNS.values()))

    pipeline_json, _ = urlretrieve(
        "https://lamindb-test.s3.amazonaws.com/pipelines.json"
    )
    with open(pipeline_json) as file:
        PIPELINES = json.load(file)
    bfxpipeline_id = _lookup(values=PIPELINES)
