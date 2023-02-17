from pathlib import Path

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore


from rich.console import Console
from rich.table import Table

from bionty.dev._io import load_yaml

console = Console()

CWD = Path.cwd()


def display_available_versions() -> None:  # pragma: no cover
    """Displays all available entities and versions in a Rich table."""
    VERSIONS_FILE_PATH = Path(f"{CWD}/bionty/versions/versions.yaml")
    versions = load_yaml(VERSIONS_FILE_PATH.resolve())

    table = _generate_rich_versions_table(title="Available versions")

    for entity, db_to_version in versions.items():
        for db, _to_versions_url in db_to_version.items():
            for _, version_to_url in _to_versions_url.items():
                for version, url in version_to_url.items():
                    table.add_row(entity, db, str(version))

    console.print(table)


def display_active_versions(
    version_table: Literal["_current.yaml", "_lndb.yaml", "_local.yaml"]
) -> None:  # pragma: no cover
    """Displays all currently set as default entities and versions in a Rich table.

    Args:
        version_table: One of '_current.yaml', '_lndb.yaml', '_local.yaml'
    """
    VERSIONS_FILE_PATH = Path(f"{CWD}/bionty/versions/{version_table}")
    versions = load_yaml(VERSIONS_FILE_PATH.resolve())

    table = _generate_rich_versions_table(
        title=f"Currently used versions in {version_table}"
    )

    for entity, db_to_version in versions.items():
        for db, version in db_to_version.items():
            table.add_row(entity, db, str(version))

    console.print(table)


def _generate_rich_versions_table(title: str) -> Table:  # pragma: no cover
    table = Table(title=title)

    table.add_column("Entity", justify="right", style="cyan", no_wrap=True)
    table.add_column("Database", justify="right", style="cyan", no_wrap=True)
    table.add_column("Version", justify="right", style="cyan", no_wrap=True)

    return table
