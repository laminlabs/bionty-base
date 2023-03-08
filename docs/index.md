```{include} ../README.md
:start-line: 0
:end-line: 5
```

Organization of biological knowledge and metadata curation.

- Lookup & curate metadata based on scientific standards.
- Access biological knowledge without the timeouts of many existing REST endpoints.
- Extend Bionty with custom ontologies or terms.

Bionty is also fully integrated into [lamin](https://lamin.ai/).

## Supported ontologies

- Gene: [Ensembl](https://ensembl.org/), [NCBI Gene](https://www.ncbi.nlm.nih.gov/gene/), [HGNC](https://www.genenames.org/), [MGI](http://www.informatics.jax.org/)
- Protein: [Uniprot](https://www.uniprot.org/)
- Species: [NCBI Taxonomy](https://www.ncbi.nlm.nih.gov/taxonomy/), [Ensembl Species](https://useast.ensembl.org/info/about/species.html)
- Cell type: [Cell Ontology](https://obophenotype.github.io/cell-ontology/)
- Cell marker: [CellMarker](http://xteam.xbio.top/CellMarker)
- Tissue: [Uberon](http://obophenotype.github.io/uberon/)
- Disease: [Mondo](https://mondo.monarchinitiative.org/), [Human Disease](https://disease-ontology.org/)
- Phenotype: [Human Phenotype](https://hpo.jax.org/app/)

## Installation

Bionty is a Python package available for ![pyversions](https://img.shields.io/pypi/pyversions/bionty)

```
pip install bionty
```

## Lookup ontology terms

```python
import bionty as bt

species = bt.Species()
species.lookup.white_tufted_ear_marmoset
```

See [lookup](guide/lookup) for more.

## Curate biological metadata such as cell types:

```python
import bionty as bt
import pandas as pd

# Create an example Pandas DataFrame of various cell types.
df = pd.DataFrame(
    index=[
        "placental epithelial cell",
        "capillary",
        "This cell type does not exist",
    ]
)

# The DataFrame can either be curated by ontology ID (id="ontology_id") or by ontology term names (id="name").
curated_df = bt.CellType(id="name").curate(df)

# ✅ 2 terms (66.7%) are linked.
# 🔶 1 terms (33.3%) are not linked.
```

See [curate](guide/curate) for more.

## Documentation:

- See the [Guide](guide/index) for in depth tutorials.
- See the [API reference](api) and the [FAQ](faq/index) for tips, edge cases & errors.
- See the [source code](https://github.com/laminlabs/bionty) on GitHub.

```{toctree}
:maxdepth: 1
:hidden:

guide/index
api
faq/index
changelog
```
