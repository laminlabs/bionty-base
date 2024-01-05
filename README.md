[![Stars](https://img.shields.io/github/stars/laminlabs/bionty?logo=GitHub&color=yellow)](https://github.com/laminlabs/bionty)
[![Coverage](https://codecov.io/gh/laminlabs/bionty/branch/main/graph/badge.svg?token=8292E0S0Z7)](https://codecov.io/gh/laminlabs/bionty)
[![pypi](https://img.shields.io/pypi/v/bionty?color=blue&label=pypi%20package)](https://pypi.org/project/bionty)

# Bionty

Access public biological ontologies.

- User docs: [here](https://lamin.ai/docs/public-ontologies)
- Developer docs: [here](https://lamin.ai/docs/bionty)

## Installation

Bionty is a Python package available for ![pyversions](https://img.shields.io/pypi/pyversions/bionty)

```shell
pip install bionty
```

## Entities

- `Gene` - [Ensembl](https://ensembl.org), [NCBI Gene](https://www.ncbi.nlm.nih.gov/gene)
- `Protein` - [Uniprot](https://www.uniprot.org/)
- `Organism` - [Ensembl Species](https://useast.ensembl.org/info/about/species.html). [NCBI Taxonomy](https://www.ncbi.nlm.nih.gov/taxonomy)
- `CellLine` - [Cell Line Ontology](https://github.com/CLO-ontology/CLO)
- `CellType` - [Cell Ontology](https://obophenotype.github.io/cell-ontology)
- `CellMarker` - [CellMarker](http://xteam.xbio.top/CellMarker)
- `Tissue` - [Uberon](http://obophenotype.github.io/uberon)
- `Disease` - [Mondo](https://mondo.monarchinitiative.org), [Human Disease](https://disease-ontology.org)
- `Phenotype` - [Human Phenotype](https://hpo.jax.org/app), [Phecodes](https://phewascatalog.org/phecodes_icd10), [PATO](https://github.com/pato-ontology/pato), [Mammalian Phenotype](http://obofoundry.org/ontology/mp.html), [Zebrafish Phenotype](http://obofoundry.org/ontology/zp.html)
- `Pathway` - [Gene Ontology](https://bioportal.bioontology.org/ontologies/GO), [Pathway Ontology](https://bioportal.bioontology.org/ontologies/PW)
- `ExperimentalFactor` - [Experimental Factor Ontology](https://www.ebi.ac.uk/ols/ontologies/efo)
- `DevelopmentalStage` - [Human Developmental Stages](https://github.com/obophenotype/developmental-stage-ontologies/wiki/HsapDv), [Mouse Developmental Stages](https://github.com/obophenotype/developmental-stage-ontologies/wiki/MmusDv)
- `Drug` - [Drug Ontology](https://bioportal.bioontology.org/ontologies/DRON)
- `Ethnicity` - [Human Ancestry Ontology](https://github.com/EBISPOT/hancestro)
- `BFXPipeline` - largely based on [nf-core](https://nf-co.re)
- `BioSample` - [NCBI BioSample attributes](https://www.ncbi.nlm.nih.gov/biosample/docs/attributes)

Check out [sources.yaml](https://github.com/laminlabs/bionty/blob/main/bionty/sources/sources.yaml) for details.

Didn't see your favorite source or version? Bionty is [extendable](https://lamin.ai/docs/bionty/guide/extend)!

## Entity versions

```python
import bionty as bt

# display currently used sources
bt.display_currently_used_sources()

# display all managed sources
bt.display_available_sources()

# local yaml file specifying all managed sources
bt.LOCAL_SOURCES

# access to the Mondo ontology
disease = bt.Disease(source="mondo")

# access to the Human Disease ontology
disease = bt.Disease(source="doid", version="2023-01-30")
```
