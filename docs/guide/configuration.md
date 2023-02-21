# Configuration

## On the various yaml files

Bionty tracks all supported and the currently active ontologies four `*.yaml` files.

1. `versions.yaml`: Stores all by Bionty supported ontologies. Users should not edit this file.
2. `local.yaml`: Stores all locally available ontologies. Users may edit this file. The file is stored at `$home:/.lamin/bionty`.
3. `._current.yaml`: Stores the currently active ontologies. Users should not edit this file.
4. `._lndb.yaml`: Stores the currently active ontologies as defined by lamindb. Users should never edit this file directly.

On startup, Bionty syncs these yaml files.
If Bionty is used for the first time the `local.yaml` file gets populated by the versions available in the most recent `versions.yaml`.
Afterwards, the `._current.yaml` file containing the current default versions gets written
using the versions that are at the top of the `._local.yaml` file.
If the user is operating in a lamindb instance, the versions specified in the `._lndb.yaml` will be used.
Alternatively, if Bionty is run in standalone mode, the versions specified in `._current.yaml` will be used.
Users may adapt the `local.yaml` with additional sources of ontologies that Bionty may not offer out of the box.

The available and currently active ontologies can also be printed to the console with
{func}`bionty.display_available_versions` or {func}`bionty.display_active_versions`.

## Setting default ontologies and versions

Since the default ontologies and versions are stored in the `._current.yaml` or the `._lndb.yaml` respectively, we can use
{func}`bionty.update_defaults` to set new defaults.
