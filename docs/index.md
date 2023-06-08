```{include} ../README.md
:start-line: 0
:end-line: 5
```

## Look up ontology records with auto-complete

```{figure} ./img/gene_lookup.png
---
width: 40%
align: left
class: with-shadow
---
```

```python
import bionty as bt

gene = bt.Gene()
gene.lookup().LNMA
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

## Track ontology sources

```python
# Display all managed versions
bt.display_available_sources()

# Access to the Mondo ontology
disease = bt.Disease(database="mondo")

# Access to the Human Disease ontology
disease = bt.Disease(database="doid", version="2023-01-30")
```

<br>

Didn't see your favorite source or version? See how to {doc}`./guide/extend`.

```{toctree}
:maxdepth: 1
:hidden:

guide/index
api
changelog
```
