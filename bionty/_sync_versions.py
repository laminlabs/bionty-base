from pathlib import Path

from .dev._io import load_yaml, write_yaml

ROOT = Path(__file__).parent / "versions"
VERSIONS = ROOT / "versions.yaml"
_LOCAL = ROOT / "_local.yaml"
_CURRENT = ROOT / "_current.yaml"

# if _local.yaml doesn't exist, copy from versions.yaml
if not _LOCAL.exists():
    import shutil

    shutil.copy2(VERSIONS, _LOCAL)
# adds entries in the public versions.yaml table to _local.yaml
versions = load_yaml(VERSIONS)
_local = load_yaml(_LOCAL)

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
    _current = {}
    for name, db_versions in versions.items():
        db = next(iter(db_versions))
        versions = db_versions.get(db).get("versions")
        version = sorted(versions.keys(), reverse=True)[0]
        _current[name] = {db: version}
    write_yaml(_current, _CURRENT)
