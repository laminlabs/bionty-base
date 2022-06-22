# Bionty: Manage biological entities

A performant & typed API for interacting with biological entities.

Normalize metadata against established scientific standards with ease.

Current backends:

- Gene: HGNC, Ensemble, biomart, mygene.
- Protein: Uniprot, Chembl, Drugbank, PDB, Ensemble.
- Species: Ensemble, NCBI Taxon.
- Tissue: Uberon.
- Disease: Mondo.
- Cell type: Cell ontology.

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

- [Quickstart](tutorial/quickstart) walks you through interacting with genes, proteins, species, and cell types.
- Check out [guides](guides/index) that address common questions, use cases or problems.
- Browse the full [API reference](api).
- See additional specific [examples](examples/index) and developer documentation.
- See the [changelog](changelog).

```{toctree}
:maxdepth: 1
:hidden:

tutorial/index
guides/index
api
examples/index
changelog
```
