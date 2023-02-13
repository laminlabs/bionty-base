import shutil
from pathlib import Path

from .dev._io import load_yaml, write_yaml

ROOT = Path(__file__).parent / "versions"
VERSIONS = ROOT / "versions.yaml"
_LOCAL = ROOT / "_local.yaml"
_CURRENT = ROOT / "_current.yaml"
_DB = ROOT / "_lndb.yaml"

versions = load_yaml(VERSIONS)


# if _local.yaml doesn't exist, copy from versions.yaml
if not _LOCAL.exists():

    def write_local_yaml(versions):
        """Make sure version keys are strings."""
        _local = {}
        for name, db_versions in versions.items():
            db = next(iter(db_versions))
            versions = db_versions.get(db).get("versions")
            _local[name] = {db: {"versions": {}}}
            for v, v_url in versions.items():
                _local[name][db]["versions"][str(v)] = v_url
        return _local

    _local = write_local_yaml(versions)
    write_yaml(_local, _LOCAL)


_local = load_yaml(_LOCAL)

# update _local to add additional entries from the public versions.yaml table
for entity, dbs in versions.items():
    if entity not in _local:
        _local[entity] = versions[entity]
    else:
        for db_name, v in dbs.items():
            if db_name not in _local[entity]:
                _local[entity][db_name] = dbs[db_name]
            else:
                for version in v["versions"]:
                    if version not in _local[entity][db_name]["versions"]:
                        _local[entity][db_name]["versions"][version] = v["versions"][
                            version
                        ]

# writes the most recent version to the _current.yaml
if not _CURRENT.exists():

    def write_current_yaml(versions):
        _current = {}
        for name, db_versions in versions.items():
            # this will only take the 1st db if multiple exists for the same entity
            db = next(iter(db_versions))
            versions = db_versions.get(db).get("versions")
            version = str(sorted(versions.keys(), reverse=True)[0])
            _current[name] = {db: version}
        return _current

    _current = write_current_yaml(versions)
    write_yaml(_current, _CURRENT)

# if no _lndb file, write _current to _lndb for lndb
if not _DB.exists():
    shutil.copy2(_CURRENT, _DB)
