from pathlib import Path

from .dev._io import load_yaml, write_yaml

ROOT = Path(__file__).parent / "versions"
VERSIONS = ROOT / "versions.yaml"
_VERSIONS = ROOT / "_versions.yaml"

# writes the most recent version to the _versions.yaml
if not _VERSIONS.exists():
    versions = load_yaml(VERSIONS)
    _versions = {}
    for name, db_versions in versions.items():
        db = next(iter(db_versions))
        versions = db_versions.get(db).get("versions")
        version = sorted(versions.keys(), reverse=True)[0]
        _versions[name] = {db: version}
    write_yaml(_versions, _VERSIONS)
