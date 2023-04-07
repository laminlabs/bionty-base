import os
from pathlib import Path
from typing import Dict, Literal, Tuple

import lamindb as ln
from rich import print

from bionty._settings import settings
from bionty.dev._io import load_yaml, write_yaml

ROOT = Path(f"{os.getcwd()}/bionty/versions")
VERSIONS_PATH = ROOT / "versions.yaml"
S3_VERSIONS_PATH = ROOT / ".s3_assets_versions.yaml"

LOCAL_PATH = settings.versionsdir / "local.yaml"


def _get_latest_ontology_files() -> Dict[str, Dict[str, Tuple[str, str]]]:
    _DYNAMIC_PATH = Path(
        f"{os.getcwd()}/.nox/build-package-bionty/lib/python3.10/site-packages/bionty/_dynamic"
    )
    entity_to_latest_ontology_dict: Dict[str, Dict[str, Tuple[str, str]]] = {}

    versions_yaml = load_yaml(VERSIONS_PATH, convert_dates=False)

    ontology_to_latest_versions: Dict[str, Dict[str, str]] = {}
    for ontology, ontology_data in versions_yaml.items():
        if ontology == "version":
            continue

        for database, version_data in ontology_data.items():
            latest_version = list(version_data["versions"].keys())[0]

            if ontology not in ontology_to_latest_versions:
                ontology_to_latest_versions[ontology] = {}
            ontology_to_latest_versions[ontology][database] = latest_version

    all_files = os.listdir(_DYNAMIC_PATH.absolute())
    for ontology, db_to_version in ontology_to_latest_versions.items():
        for latest_database, latest_version in db_to_version.items():

            for filename in all_files:
                if (
                    ontology in filename
                    and latest_database in filename
                    and latest_version in filename
                ):
                    if ontology not in entity_to_latest_ontology_dict:
                        entity_to_latest_ontology_dict[ontology] = {}
                    entity_to_latest_ontology_dict[ontology][latest_database] = (
                        latest_version,
                        os.path.join(_DYNAMIC_PATH.absolute(), filename),
                    )

    return entity_to_latest_ontology_dict


def _upload_ontology_artifacts(
    instance: str,
    entity_to_latest_ontology: Dict[str, Dict[str, Tuple[str, str]]],
    source: Literal["versions", "local"] = "versions",
):
    versions_yaml = (
        load_yaml(VERSIONS_PATH, convert_dates=False)
        if source == "versions"
        else load_yaml(LOCAL_PATH, convert_dates=False)
    )

    ln.setup.login(
        "testuser2@lamin.ai", password="goeoNJKE61ygbz1vhaCVynGERaRrlviPBVQsjkhz"
    )
    ln.setup.load(instance, migrate=True)
    with ln.Session() as ss:
        transform = ln.add(ln.Transform, name="Bionty ontology artifacts upload")
        run = ln.Run(transform=transform)

        for entity, db_to_version_path in entity_to_latest_ontology.items():
            for db, version_path in db_to_version_path.items():
                latest_path = version_path[1]

                # TODO Remove the file extension code as soon as File uses the full filename.
                file_name = latest_path.split("/")[-1]
                file_name_no_extension = file_name.split(".")[0]
                ontology_ln_file = ss.select(
                    ln.File, name=file_name_no_extension
                ).one_or_none()

                if ontology_ln_file is not None:
                    print(
                        "[bold yellow]Found"
                        f" {ontology_ln_file.name}{ontology_ln_file.suffix} on S3."
                        " Skipping ingestion..."
                    )
                else:
                    ontology_ln_file = ln.File(latest_path, source=run)
                    ss.add(ontology_ln_file)

                s3_path_ID = str(ontology_ln_file.load()).split("/")[-1]
                species, database, version, class_entity = latest_path.split("___")
                version = str(version)

                S3_BASE_URL = "s3://bionty-assets-test/"

                versions_yaml[class_entity][database]["versions"][version][2] = (
                    S3_BASE_URL + s3_path_ID
                )

    write_yaml(versions_yaml, VERSIONS_PATH)


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
