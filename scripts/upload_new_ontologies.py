import os
from pathlib import Path
from typing import Dict, Literal

import lamindb as ln
from rich import print

from bionty import Entity
from bionty._settings import settings
from bionty.dev._io import load_yaml, write_yaml

ROOT = Path(__file__).parent / "bionty/versions"
VERSIONS_PATH = ROOT / "versions.yaml"
S3_VERSIONS_PATH = ROOT / ".s3_assets_versions.yaml"
_CURRENT_PATH = ROOT / "._current.yaml"
_LNDB_PATH = ROOT / "._lndb.yaml"

LOCAL_PATH = settings.versionsdir / "local.yaml"


def _get_latest_ontology_files() -> Dict[str, str]:
    _DYNAMIC_PATH = Path(
        f"{os.getcwd()}/.nox/build-package-bionty/lib/python3.9/site-packages/bionty/_dynamic"
    )
    entity_to_latest_ontology = {}
    for cls in Entity.__subclasses__():
        latest_file = None
        latest_date = None

        for filename in os.listdir(_DYNAMIC_PATH.absolute()):
            if cls.__name__ in filename:
                file_date = os.path.getmtime(
                    os.path.join(_DYNAMIC_PATH.absolute(), filename)
                )
                if latest_date is None or file_date > latest_date:
                    latest_file = filename
                    latest_date = file_date

        if latest_file is not None:
            latest_file_path = os.path.join(_DYNAMIC_PATH.absolute(), latest_file)
            entity_to_latest_ontology[cls.__name__] = latest_file_path
        else:
            print(
                f"[bold yellow]No matching files found for Entity [blue]{cls.__name__}."
            )

    return entity_to_latest_ontology


def _upload_ontology_artifacts(
    instance: str,
    entity_to_latest_ontology: Dict[str, str],
    source: Literal["versions", "local"] = "versions",
):
    versions_yaml = (
        load_yaml(VERSIONS_PATH) if source == "versions" else load_yaml(LOCAL_PATH)
    )

    ln.setup.login(
        "testuser2@lamin.ai", password="goeoNJKE61ygbz1vhaCVynGERaRrlviPBVQsjkhz"
    )
    ln.setup.load(instance, migrate=True)
    with ln.Session() as ss:
        transform = ln.add(ln.Transform, name="Bionty ontology artifacts upload")
        run = ln.Run(transform=transform)

        for entity, ontology_path in entity_to_latest_ontology.items():
            # TODO Remove the file extension code as soon as File uses the full filename.
            file_name = ontology_path.split("/")[-1]
            file_name_no_extension = file_name.split(".")[0]
            ontology_ln_file = ss.select(
                ln.File, name=file_name_no_extension
            ).one_or_none()

            if ontology_ln_file is not None:
                print(
                    "[bold yellow]Found"
                    f" {ontology_ln_file.name}{ontology_ln_file.suffix} on S3. Skipping"
                    " ingestion..."
                )
            else:
                ontology_ln_file = ln.File(ontology_path, source=run)
                ss.add(ontology_ln_file)

            s3_path_ID = str(ontology_ln_file.load()).split("/")[-1]
            species, database, version, class_entity = ontology_path.split("___")

            S3_BASE_URL = "s3://bionty-assets-test/"

            versions_yaml[class_entity][database]["versions"][version][0] = (
                S3_BASE_URL + s3_path_ID
            )

    write_yaml(versions_yaml, S3_VERSIONS_PATH)


def _run_update_version_url(instance: str, check_github: bool = True) -> None:
    if check_github:
        if (
            os.environ["GITHUB_EVENT_NAME"] != "push"
            or os.environ["GITHUB_REF"] != "main"
        ):
            return

    entity_to_latest_ontology_dict = _get_latest_ontology_files()
    _upload_ontology_artifacts(
        instance=instance, entity_to_latest_ontology=entity_to_latest_ontology_dict
    )


_run_update_version_url(instance="bionty-assets-test", check_github=False)
