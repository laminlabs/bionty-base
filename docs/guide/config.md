# Configuration

## On the various yaml files

Bionty tracks all supported and the currently active ontologies four `*.yaml` files.

1. `sources.yaml`: Stores all Bionty supported public ontologies. Users should not edit this file.
2. `sources.local.yaml`: Stores all locally available ontologies. **Users may edit this file.** The file is stored at `$home:/.lamin/bionty`.
3. `.currently_used_sources.yaml`: Stores the currently active ontologies. Users should not edit this file.
4. `.lamindb_setup.yaml`: Stores the currently active ontologies as defined by lamindb. Users should never edit this file directly.

On startup, Bionty syncs these yaml files.
If Bionty is used for the first time the `sources.local.yaml` file gets populated by the versions available in the most recent `sources.yaml`.
Afterwards, the `.currently_used_sources.yaml` file containing the current default versions gets written
using the versions that are at the top of the `.sources.local.yaml` file.
If the user is operating in a lamindb instance, the versions specified in the `.lamindb_setup.yaml` will be used.
Alternatively, if Bionty is run in standalone mode, the versions specified in `.currently_used_sources.yaml` will be used.
Users may adapt the `sources.local.yaml` with additional sources of ontologies that Bionty may not offer out of the box.

The available and currently active ontologies can also be printed to the console with
{func}`bionty.display_available_sources` or {func}`bionty.display_currently_used_sources`.

## Setting default ontologies and versions

The first entry in `sources.local.yaml` is used as default. To set your own default ontology and version, shift the order of entries.

For example, in the following "doid" used when "species" is specified as "human":

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

We may change the default to "inhouse_diseases" when "species" is specified as "human", by the following:

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
  inhouse_diseases:
    human:
      2000-01-01:
        source: http://download-my-diseases.com/releases/2000-01-01/mydiseases.owl
        md5: "md5 if available or leave out this row"
    name: My in-house Disease Ontology
    website: http://my-website.com
  doid:
    human:
      2023-01-30:
        source: http://purl.obolibrary.org/obo/doid/releases/2023-01-30/doid.obo
        md5: 9f0c92ad2896dda82195e9226a06dc36
    name: Human Disease Ontology
    website: https://disease-ontology.org/
```
