from pathlib import Path

from .dev._io import load_yaml, write_yaml

_VERSIONS_PATH = Path(__file__).parent / "_versions.yml"

# writes the most recent version to the _versions.yml
if not _VERSIONS_PATH.exists():
    versions = load_yaml("versions.yml")
    _versions = {}
    for name, db_versions in versions.items():
        db = next(iter(db_versions))
        versions = db_versions.get(db).get("versions")
        version = sorted(versions.keys(), reverse=True)[0]
        _versions[name] = {db: version}
    write_yaml(_versions, _VERSIONS_PATH)
