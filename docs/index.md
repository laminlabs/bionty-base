```{include} ../README.md
:start-line: 0
:end-line: 4
```

_For background, see [Lamin Blog #4 (2022)](https://lamin.ai/notes/2022/bionty)._

Lookup & curate metadata based on scientific standards.

- Gene: [Ensembl](https://ensembl.org/), [NCBI Gene](https://www.ncbi.nlm.nih.gov/gene/), [HGNC](https://www.genenames.org/), [MGI](http://www.informatics.jax.org/).
- Protein: [Uniprot](https://www.uniprot.org/).
- Species: [NCBI Taxonomy](https://www.ncbi.nlm.nih.gov/taxonomy/), [Ensembl Species](https://useast.ensembl.org/info/about/species.html).
- Cell type: [Cell Ontology](https://obophenotype.github.io/cell-ontology/).
- Cell marker: [CellMarker](http://xteam.xbio.top/CellMarker).
- Tissue: [Uberon](http://obophenotype.github.io/uberon/).
- Disease: [Mondo](https://mondo.monarchinitiative.org/).

```{Note}

- For a full data & analysis management system that integrates Bionty, consider [LaminDB](https://lamin.ai/docs/db).
- More complex queries of relationships among entities are on the roadmap.
```

Install:

```
pip install bionty
```

Get started:

- The [tutorials](tutorials/index) walk you through curating and looking up entities.
- Browse the full [API reference](api).
- Check out [guides](guides/index) that address common questions, use cases or problems.
- Check out [bionty-assets](https://lamin.ai/docs/bionty-assets) for how entity tables are curated.
- See the [changelog](changelog) for feature updates.

```{toctree}
:maxdepth: 1
:hidden:

tutorials/index
api
guides/index
changelog
```
