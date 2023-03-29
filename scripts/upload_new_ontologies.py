import os
from pathlib import Path
from typing import Dict

import lamindb as ln
from rich import print

from bionty import Entity


def _get_latest_ontology_files() -> Dict[str, str]:
    _DYNAMIC_PATH = Path(
        f"{os.getcwd()}/.nox/build-package-bionty/lib/python3.10/site-packages/bionty/_dynamic"
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
            print(f"[bold yellow]No matching files found for {cls.__name__}.")

    return entity_to_latest_ontology


def _upload_ontology_artifacts(entity_to_latest_ontology: Dict[str, str]):
    ln.setup.load("testuser1/lamin-site-assets", migrate=True)
    with ln.Session() as ss:
        transform = ln.add(ln.Transform, name="Bionty ontology artifacts upload")
        run = ln.Run(transform=transform)

        for entity, ontology_path in entity_to_latest_ontology.items():
            ontology_ln_file = ss.select(ln.File, name=ontology_path).one_or_none()
            if ontology_ln_file is not None:
                ontology_ln_file._cloud_filepath = None
                ontology_ln_file._local_filepath = Path(ontology_path)
                ontology_ln_file.source = run
            else:
                ontology_ln_file = ln.File(ontology_path, source=run)
            ss.add(ontology_ln_file)


def _run_upload():
    if os.environ["GITHUB_EVENT_NAME"] != "push" or os.environ["GITHUB_REF"] != "main":
        return

    entity_to_latest_ontology = _get_latest_ontology_files()
    _upload_ontology_artifacts(entity_to_latest_ontology)


_run_upload()
