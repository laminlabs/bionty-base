[![Stars](https://img.shields.io/github/stars/laminlabs/bionty?logo=GitHub&color=yellow)](https://github.com/laminlabs/bionty)
[![Coverage](https://codecov.io/gh/laminlabs/bionty/branch/main/graph/badge.svg?token=8292E0S0Z7)](https://codecov.io/gh/laminlabs/bionty)
[![pypi](https://img.shields.io/pypi/v/bionty?color=blue&label=pypi%20package)](https://pypi.org/project/bionty)

# Bionty

Biological ontologies for data scientists: look up, search, inspect, and map terms.

To manage custom bio-registries along with public ontologies, see this LaminDB guide: {doc}`docs:biology/registries`.

## Entities

- `Gene` - [Ensembl](https://ensembl.org/), [NCBI Gene](https://www.ncbi.nlm.nih.gov/gene/), [HGNC](https://www.genenames.org/), [MGI](http://www.informatics.jax.org/)
- `Protein` - [Uniprot](https://www.uniprot.org/)
- `Species` - [NCBI Taxonomy](https://www.ncbi.nlm.nih.gov/taxonomy/), [Ensembl Species](https://useast.ensembl.org/info/about/species.html)
- `CellLine` - [Cell Line Ontology](https://github.com/CLO-ontology/CLO)
- `CellType` - [Cell Ontology](https://obophenotype.github.io/cell-ontology/)
- `CellMarker` - [CellMarker](http://xteam.xbio.top/CellMarker)
- `Tissue` - [Uberon](http://obophenotype.github.io/uberon/)
- `Disease` - [Mondo](https://mondo.monarchinitiative.org/), [Human Disease](https://disease-ontology.org/)
- `Phenotype` - [Human Phenotype](https://hpo.jax.org/app/), [Mammalian Phenotype](http://obofoundry.org/ontology/mp.html), [Zebrafish Phenotype](http://obofoundry.org/ontology/zp.html)
- `Pathway` - [Gene Ontology](https://bioportal.bioontology.org/ontologies/GO), [Pathway Ontology](https://bioportal.bioontology.org/ontologies/PW)
- `ExperimentalFactor` - [Experimental Factor Ontology](https://www.ebi.ac.uk/ols/ontologies/efo)
- `Drug` - [Drug Ontology](https://bioportal.bioontology.org/ontologies/DRON)
- `BFXPipeline` - largely based on [nf-core](https://nf-co.re/)

Check out [sources.yaml](https://github.com/laminlabs/bionty/blob/main/bionty/sources/sources.yaml) for details.

Didn't see your favorite source or version? Bionty is [extendable](https://lamin.ai/docs/bionty/extend)!

## Installation

Bionty is a Python package available for ![pyversions](https://img.shields.io/pypi/pyversions/bionty)

```shell
pip install bionty
```

## Usage overview & quickstart

```python
import bionty as bt
```

### Look up terms with auto-complete

```python
lookup = bt.ExperimentalFactor().lookup()
# access via Python-friendly keys
lookup.single_cell_rna_sequencing

# access via dictionary
lookup_dict = lookup.dict()
lookup_dict["single-cell RNA sequencing"]
```

### Search ontology terms

```python
celltype_bionty = bt.CellType()
# Free text search against a field
celltype_bionty.search("gamma delta T cell")
```

### Inspect & map terms

```python
gene_bionty = bt.Gene()
# Inspect if the gene symbols are mappable onto the reference
gene_bionty.inspect(["A1BG", "FANCD1"], gene_bionty.symbol)
# Map synonyms of gene symbols
gene_bionty.map_synonyms(["A1BG", "FANCD1"])
```

### Access a reference DataFrame

```python
# Reference table of the human genes
df = bt.Gene(species="human").df()
```

### Track ontology sources

```python
# Display currently used sources
bt.display_currently_used_sources()

# Display all managed sources
bt.display_available_sources()

# Local yaml file specifying all managed sources
bt.LOCAL_SOURCES

# Access to the Mondo ontology
disease = bt.Disease(source="mondo")

# Access to the Human Disease ontology
disease = bt.Disease(source="doid", version="2023-01-30")
```

## Documentation

Read the [docs](https://lamin.ai/docs/bionty/).
