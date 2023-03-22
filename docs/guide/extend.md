# Extend Bionty

Bionty is designed to be extendable in various ways. This guide covers how to:

1. Extend existing ontologies such as adding a new cell type to a cell type ontology
2. Adding new ontologies such as a new disease ontology
3. Implementing new entities that Bionty does not cover

## New terms and records

If you'd like to add new terms to an existing ontology we recommend using [Lamin](https://lamin.ai/docs) to enable full knowledge management features.
A work in progress tutorial can be found [here](https://lamin.ai/docs/lnschema-bionty/guide/tables).
For use cases where Bionty is run standalone, we kindly ask users to be patience since support for it is currently work in progress.

## New ontologies

The easiest way to add new ontologies or versions to existing entities is to adapt the `local.yml` file in the `$home/.lamin/bionty/versions` directory.
For example, to add a new disease ontology (termed "mydiseases") with an associated version and URL, one adds the following lines to the `local.yml`.

```yaml
Disease:
  mondo:
    versions:
      2023-02-06:
        [
          "http://purl.obolibrary.org/obo/mondo/releases/2023-02-06/mondo.owl",
          "2b7d479d4bd02a94eab47d1c9e64c5db",
        ]
      2022-10-11:
        [
          "http://purl.obolibrary.org/obo/mondo/releases/2022-10-11/mondo.owl",
          "04b808d05c2c2e81430b20a0e87552bb",
        ]
    name: Mondo Disease Ontology
    website: https://mondo.monarchinitiative.org/
  doid:
    versions:
      2023-01-30:
        [
          "http://purl.obolibrary.org/obo/doid/releases/2023-01-30/doid.obo",
          "9f0c92ad2896dda82195e9226a06dc36",
        ]
    name: Human Disease Ontology
    website: https://disease-ontology.org/
  mydiseases:
    versions:
      2000-01-01:
        [
          "http://download-my-diseases.com/releases/2000-01-01/mydiseases.owl",
          "md5 if available or empty string otherweise",
        ]
    name: My Disease Ontology
    website: http://some-website.com
```

The md5 sum is optional (leave empty if not available) and can be calculated with for example:

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

Adding new entities to Bionty requires subclassing the {class}`bionty.Entity` and modifying the `local.yml` file.

The {class}`bionty.Entity` requires several properties to be defined:

```python
species: str,
database: str,
version: str,
```

These are automatically populated by either the `._current.yaml` (see {doc}`./config`) or explicitly passed as parameters when initializing an Entity.

Hence, a new Entity `MyEntity` would be defined as:

```python
from bionty import Entity

class MyEntity(Entity):
    """MyEntity."""

    def __init__(
        self,
        species: str = "human",
        database: str | None = None,
        version: str | None = None,
    ) -> None:
        super().__init__(
            database=database,
            version=version,
            species=species,
        )
```

The `local.yml` would then need to be extended as:

```yaml
MyEntity:
  mydatabase_1:
    versions:
      2042-01-01:
        [
          "http://my-url/releases/2042-01-01/mydatabase_1.owl",
          "md5 if available or empty string otherweise",
        ]
  mydatabase_2:
    versions:
      2042-01-01:
        [
          "http://my-url/releases/2042-01-01/mydatabase_2.owl",
          "md5 if available or empty string otherweise",
        ]
```

If the ontology file is not a standard `*.owl` file, the generation of the Pandas DataFrame might require custom code. In this case the function:

```python
    @cached_property
    def df(self) -> pd.DataFrame:
        """Pandas DataFrame."""
        self._filepath = settings.datasetdir / self.filenames.get(
            f"{self.species}_{self.database}"
        )

        if not self._filepath.exists():
            df = self._ontology_to_df(self.ontology)
            df.to_parquet(self._filepath)

        return pd.read_parquet(self._filepath)
```

should be overwritten in the Entity class:

```python
    @cached_property
    def df(self) -> pd.DataFrame:
        """Pandas DataFrame."""
        # TODO: Implement me
        pass
        return pd.DataFrame()
```

Great! Now we've added a new Entity, which can be used with all Bionty functions! 🎉
