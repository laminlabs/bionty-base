```{include} ../README.md
:start-line: 0
:end-line: 4
```

_For background, see [Lamin Blog #4 (2022)](https://lamin.ai/notes/2022/bionty)._

Lookup & curate metadata based on scientific standards.

- Gene: [HGNC](https://www.genenames.org/), [MGI](http://www.informatics.jax.org/), [Ensembl](https://ensembl.org/), [NCBI Gene](https://www.ncbi.nlm.nih.gov/gene/).
- Protein: [Uniprot](https://www.uniprot.org/), [Chembl](https://www.ebi.ac.uk/chembl/), [Drugbank](https://go.drugbank.com/), [PDB](http://www.wwpdb.org/).
- Species: [Ensembl](https://useast.ensembl.org/info/about/species.html), [NCBI Taxonomy](https://www.ncbi.nlm.nih.gov/taxonomy/).
- Tissue: [Uberon](http://obophenotype.github.io/uberon/).
- Disease: [Mondo](https://mondo.monarchinitiative.org/).
- Cell type: [Cell Ontology](https://obophenotype.github.io/cell-ontology/).

```{Note}

- For a full data & analysis management system that integrates Bionty, consider [LaminDB](https://lamin.ai/lamindb).
- More complex queries of relationships among entities are on the roadmap.
```

Install:

```
pip install bionty
```

Get started:

- The [tutorials](tutorials/index) walk you through curating and looking up genes, proteins, species, and cell types.
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
