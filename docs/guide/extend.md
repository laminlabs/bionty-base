# Extend Bionty

Bionty is designed to be extendable in various ways. This guide covers how to:

1. Extend existing ontologies such as adding a new cell type to a cell type ontology
2. Adding new ontologies such as a new disease ontology
3. Implementing new entities that Bionty does not cover

## New terms and records

If you'd like to add new terms to an existing ontology we recommend using [Lamin](https://lamin.ai/docs) to enable full knowledge management features.

For use cases where Bionty is run standalone, we kindly ask users to be patience since support for it is currently work in progress.

## New ontologies

The easiest way to add new ontologies to existing entities is to adapt the `sources.local.yaml` file in the `$home/.lamin/bionty/sources` directory.
For example, to add a new disease ontology (termed "inhouse_diseases") with an associated version and URL, one adds the following lines to the `sources.local.yaml`.

```yaml
Disease:
  mondo:
    all:
      2023-02-06:
        source: http://purl.obolibrary.org/obo/mondo/releases/2023-02-06/mondo.owl
        md5: 2b7d479d4bd02a94eab47d1c9e64c5db
      2022-10-11:
        source: http://purl.obolibrary.org/obo/mondo/releases/2022-10-11/mondo.owl
        md5: 04b808d05c2c2e81430b20a0e87552bb
    name: Mondo Disease Ontology
    website: https://mondo.monarchinitiative.org/
  doid:
    human:
      2023-01-30:
        source: http://purl.obolibrary.org/obo/doid/releases/2023-01-30/doid.obo
        md5: 9f0c92ad2896dda82195e9226a06dc36
    name: Human Disease Ontology
    website: https://disease-ontology.org/
  inhouse_diseases:
    human:
      2000-01-01:
        source: http://download-my-diseases.com/releases/2000-01-01/mydiseases.owl
        md5: "md5 if available or leave out this row"
    name: My in-house Disease Ontology
    website: http://my-website.com
```

Use "all" if species doesn't apply or unknown.

The md5 sum is optional (leave out if not available) and can be calculated with for example:

```python
import hashlib
from pathlib import Path

def calculate_md5(file_path: Path | str) -> str:
    with open(file_path, "rb") as f:
        md5 = hashlib.md5()
        while True:
            data = f.read(8192)
            if not data:
                break
            md5.update(data)
        file_md5 = md5.hexdigest()
    print(file_md5)
```

If desired, the new ontology can be set as default. See {doc}`./config` for more details.

## New entites

Adding new entities to Bionty requires subclassing the {class}`bionty.Bionty` and modifying the `sources.local.yaml` file.

The {class}`bionty.Bionty` requires several properties to be defined:

```python
species: str,
source: str,
version: str,
```

These are automatically populated by either the currently used Bionty sources (see {doc}`./config`) or explicitly passed as parameters when initializing an Entity.

Hence, a new Bionty class `MyEntity` would be defined as:

```python
from bionty import Bionty


class MyEntity(Bionty):
    """MyEntity."""

    def __init__(
        self,
        species: Optional[str] = None,
        source: Optional[Literal["mydatabase_1", "mydatabase_2"]] = None,
        version: Optional[str] = None,
        **kwargs
    ) -> None:
        super().__init__(
            source=source,
            version=version,
            species=species,
            **kwargs
        )
```

The `local.yml` would then need to be extended as:

```yaml
MyEntity:
  mysource_1:
    human:
      2042-01-01:
        source: http://my-url/releases/2042-01-01/mysource_1.owl
        md5: "md5 if available or leave out this row"
  mysource_2:
    all:
      2042-01-01:
        source: http://my-url/releases/2042-01-01/mysource_2.owl
        md5: "md5 if available or leave out this row"
```

Great! Now we've added a new Bionty class, which can be used with all Bionty functions! 🎉
