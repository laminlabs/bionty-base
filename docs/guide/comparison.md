# Relating Bionty to other tools

Biological ontologies are structured frameworks that define and categorize biological entities along with the relationships that connect them.
Knowledge graphs, built upon these ontologies, extend this concept by creating interconnected networks of biological entities,
fostering a holistic understanding of complex biological systems.
Here, we will describe the similarities and differences between Bionty and other tools.

## Bionty

[Bionty](https://lamin.ai/docs/bionty) is a Python package that provides unified access to biological ontologies.
It further provides an API to curate biological metadata in standalone mode and as an SQL plugin as part of the [Lamin platform](https://lamin.ai/).
In-house ontologies can extend Bionty to enable the curation of previously unseen biological data.
[Bionty](https://lamin.ai/docs/bionty) is not designed to build ontologies or knowledge graphs.

## Biolink

[BioLink](https://biolink.github.io/biolink-model/) is a standardized data model designed to facilitate the integration and querying of biological data from various sources in knowledge graphs.
It provides a structured way to represent biological entities, their attributes, and the relationships between them, enhancing interoperability in bioinformatics.
The [Biolink Model](https://biolink.github.io/biolink-model/) is primarily a schema in YAML syntax that is translated into various formats.
[BioLink](https://biolink.github.io/biolink-model/) does not provide tooling to access the generated knowledge graphs.

## Biocypher

[Biocypher](https://biocypher.org/) is a Python package that simplifies the creation of knowledge graphs.
Based on a modular structure, [Biocypher](https://biocypher.org/) allows for the manipulation and harmonization of ontologies.
[Biocypher](https://biocypher.org/) does not focus on data curation or SQL entities and is primarily for developers interested in building their own ontologies.
