[![Stars](https://img.shields.io/github/stars/laminlabs/bionty?logo=GitHub&color=yellow)](https://github.com/laminlabs/bionty)
[![Coverage](https://codecov.io/gh/laminlabs/bionty/branch/main/graph/badge.svg?token=8292E0S0Z7)](https://codecov.io/gh/laminlabs/bionty)
[![pypi](https://img.shields.io/pypi/v/bionty?color=blue&label=pypi%20package)](https://pypi.org/project/bionty)

# Bionty: Basic biological entities

Access public & custom ontologies with auto-complete. Map synonyms with ease.

To manage in-house bioregistries along with ontologies, see [lnschema_bionty](https://lamin.ai/docs/lnschema-bionty).

## Out-of-the-box ontologies

- `Gene` - [Ensembl](https://ensembl.org/), [NCBI Gene](https://www.ncbi.nlm.nih.gov/gene/), [HGNC](https://www.genenames.org/), [MGI](http://www.informatics.jax.org/)
- `Protein` - [Uniprot](https://www.uniprot.org/)
- `Species` - [NCBI Taxonomy](https://www.ncbi.nlm.nih.gov/taxonomy/), [Ensembl Species](https://useast.ensembl.org/info/about/species.html)
- `CellLine` - [Cell Line Ontology](https://github.com/CLO-ontology/CLO)
- `CellType` - [Cell Ontology](https://obophenotype.github.io/cell-ontology/)
- `CellMarker` - [CellMarker](http://xteam.xbio.top/CellMarker)
- `Tissue` - [Uberon](http://obophenotype.github.io/uberon/)
- `Disease` - [Mondo](https://mondo.monarchinitiative.org/), [Human Disease](https://disease-ontology.org/)
- `Phenotype` - [Human Phenotype](https://hpo.jax.org/app/)
- `Pathway` - [Gene Ontology](https://bioportal.bioontology.org/ontologies/GO), [Pathway Ontology](https://bioportal.bioontology.org/ontologies/PW)
- `Readout` - [Experimental Factor Ontology](https://www.ebi.ac.uk/ols/ontologies/efo)
- `BFXPipeline` - largely based on [nf-core](https://nf-co.re/)

Check out [sources.yaml](https://github.com/laminlabs/bionty/blob/main/bionty/versions/sources.yaml) for details.

## Installation

Bionty is a Python package available for ![pyversions](https://img.shields.io/pypi/pyversions/bionty)

```shell
pip install bionty
```

## Look up ontology records with auto-complete

```python
import bionty as bt

gene = bt.Gene()
gene.lookup().LNMA
```

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

Didn't see your favorite source or version? Bionty is extendable!

## Documentation

Read the [docs](https://lamin.ai/docs/bionty/).
