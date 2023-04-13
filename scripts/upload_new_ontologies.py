import os
from pathlib import Path

import lamindb as ln
from rich import print


def _upload_ontology_artifacts(
    instance: str, lndb_user: str, lndb_password: str, python_version: str = "3.10"
):
    _DYNAMIC_PATH = Path(
        f"{os.getcwd()}/.nox/build-package-bionty/lib/python{python_version}/site-packages/bionty/_dynamic"
    )

    ln.setup.login(lndb_user, password=lndb_password)
    ln.setup.load(instance, migrate=True)
    with ln.Session() as ss:
        transform = ln.add(ln.Transform, name="Bionty ontology artifacts upload")
        run = ln.Run(transform=transform)

        for filename in os.listdir(_DYNAMIC_PATH.absolute()):
            nox_ontology_file_path = os.path.join(_DYNAMIC_PATH.absolute(), filename)

            ontology_ln_file = ss.select(ln.File, name=filename).one_or_none()

            if ontology_ln_file is not None:
                print(
                    "[bold yellow]Found"
                    f" {ontology_ln_file.name}{ontology_ln_file.suffix} on S3."
                    " Skipping ingestion..."
                )
            else:
                ontology_ln_file = ln.File(
                    nox_ontology_file_path, key=filename, source=run
                )
                ss.add(ontology_ln_file)


def _run_update_version_url(instance: str, check_github: bool = True) -> None:
    if check_github:
        if (
            os.environ["GITHUB_EVENT_NAME"] != "push"
            or os.environ["GITHUB_REF"] != "main"
        ):
            return

    _upload_ontology_artifacts(
        instance=instance,
        lndb_user="testuser2@lamin.ai",
        lndb_password="goeoNJKE61ygbz1vhaCVynGERaRrlviPBVQsjkhz",
        python_version="3.10",
    )


# TODO Change the URL when going into production
_run_update_version_url(instance="bionty-assets-test", check_github=False)
