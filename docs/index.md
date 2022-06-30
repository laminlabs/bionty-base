```{include} ../README.md
:start-line: 0
:end-line: 4
```

_Open data model for biology._

A performant API for interacting with biological entities.
Normalize metadata against established scientific standards with ease.

Current backends:

- Gene: [HGNC](https://www.genenames.org/), [VGNC](https://vertebrate.genenames.org/), [Ensembl](https://ensembl.org/), [biomart](https://ensembl.org/info/data/biomart/), [mygene](https://mygene.info/).
- Protein: [Uniprot](https://www.uniprot.org/), [Chembl](https://www.ebi.ac.uk/chembl/), [Drugbank](https://go.drugbank.com/), [PDB](http://www.wwpdb.org/).
- Species: [Ensembl](https://useast.ensembl.org/info/about/species.html), [NCBI Taxonomy](https://www.ncbi.nlm.nih.gov/taxonomy/).
- Tissue: [Uberon](http://obophenotype.github.io/uberon/).
- Disease: [Mondo](https://mondo.monarchinitiative.org/).
- Cell type: [Cell Ontology](https://obophenotype.github.io/cell-ontology/).

```{Note}

- For a full data & analysis management system that integrates Bionty, consider [LaminDB](https://lamin.ai/lamindb).
- More complex queries of relationships among entities are on the roadmap.
- Eventually, we hope that an open API will enable collaborative data science across organizations at scale.
```

Install:

```
pip install bionty
```

Get started:

- [Quickstart](tutorials/quickstart) walks you through interacting with genes, proteins, species, and cell types.
- Browse the full [API reference](api).
- Check out [guides](guides/index) that address common questions, use cases or problems.
- See the [changelog](changelog).

```{toctree}
:maxdepth: 1
:hidden:

tutorials/index
api
guides/index
changelog
```
