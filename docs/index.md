```{include} ../README.md
:start-line: 0
:end-line: 5
```

- Look up records with autocompletion.
- Map, curate and standardize metadata.
- Manage public & custom ontologies and their versions.

To query, collaborate on, and persistently store knowledge & data, consider [Bionty's SQL interface](https://lamin.ai/docs/lnschema-bionty/) with [LaminDB](https://lamin.ai/docs/) - open-source data lake for biology.

## Out-of-the-box ontologies

- Gene: [Ensembl](https://ensembl.org/), [NCBI Gene](https://www.ncbi.nlm.nih.gov/gene/), [HGNC](https://www.genenames.org/), [MGI](http://www.informatics.jax.org/)
- Protein: [Uniprot](https://www.uniprot.org/)
- Species: [NCBI Taxonomy](https://www.ncbi.nlm.nih.gov/taxonomy/), [Ensembl Species](https://useast.ensembl.org/info/about/species.html)
- CellLine: [Cell Line Ontology](https://github.com/CLO-ontology/CLO)
- CellType: [Cell Ontology](https://obophenotype.github.io/cell-ontology/)
- CellMarker: [CellMarker](http://xteam.xbio.top/CellMarker)
- Tissue: [Uberon](http://obophenotype.github.io/uberon/)
- Disease: [Mondo](https://mondo.monarchinitiative.org/), [Human Disease](https://disease-ontology.org/)
- Phenotype: [Human Phenotype](https://hpo.jax.org/app/)
- Pathway: [Pathway Ontology](https://bioportal.bioontology.org/ontologies/PW)
- Readout: [Experimental Factor Ontology](https://www.ebi.ac.uk/ols/ontologies/efo)

Check out [versions.yaml](https://github.com/laminlabs/bionty/blob/main/bionty/versions/versions.yaml) for details.

## Installation

Bionty is a Python package available for ![pyversions](https://img.shields.io/pypi/pyversions/bionty)

```shell
pip install bionty
```

## Import

In your python script, import Bionty as:

```python
import bionty as bt
```

## Look up ontology terms with autocompletion

```{figure} ./img/gene_lookup.png
---
width: 40%
align: left
class: with-shadow
---
```

```python
gene = bt.Gene()
gene.lookup.LNMA
```

<br>

See {doc}`./guide/lookup` for more.

## Curate metadata

```python
import pandas as pd

# Create an example Pandas DataFrame of various cell types.
df = pd.DataFrame(
    index=[
        "placental epithelial cell",
        "capillary",
        "This cell type does not exist",
    ]
)

# The DataFrame can either be curated by ontology ID (id="ontology_id")
# or by ontology term names (id="name").
curated_df = bt.CellType(id="name").curate(df)

# ✅ 2 terms (66.7%) are mapped.
# 🔶 1 terms (33.3%) are not mapped.
```

<br>

See {doc}`./guide/curate` for more.

## Access ontology databases and versions

```python
# Display all managed versions
bt.display_available_versions()

# Access to the Mondo ontology
disease = bt.Disease(database="mondo")

# Access to the Human Disease ontology
disease = bt.Disease(database="doid", version="2023-01-30")
```

<br>

Didn't see your favorite database or version? See how to {doc}`./guide/extend`.

```{toctree}
:maxdepth: 1
:hidden:

guide/index
api
faq/index
changelog
```
