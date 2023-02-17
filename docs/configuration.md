# Configuration

## On the various yaml files

Bionty tracks all supported and the currently active ontologies four `*.yaml` files.

1. `versions.yaml`: Stores all available ontologies. Users should not edit this file.
2. `_current.yaml`: Stores the currently active ontologies. Users should never edit this file.
3. `_lndb.yaml`: Stores the currently active ontologies as defined by lamindb. Users should never edit this file.
4. `_local.yaml`: Stores all locally available ontologies. Users may edit this file.

On startup, Bionty syncs these yaml files. If the user is operating in a lamindb instance,
the versions specified in the `_lndb.yaml` will be used.
Alternatively, if Bionty is run in standalone mode, the versions specified in `_current.yaml` will be used.
Users may adapt the `_local.yaml` with additional sources of ontologies that Bionty may not offer out of the box.

The available and currently active ontologies can also be printed to the console with
{func}`bionty.display_available_versions` or {func}`bt.display_active_versions`.

## Setting default ontologies

Details will be added soon.

## Initializing bionty's defaults for all lamindb instances

Details will be added soon.
