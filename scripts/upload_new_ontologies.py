import os
from pathlib import Path

import lamindb as ln
from rich import print


def _upload_ontology_artifacts(
    instance: str, lndb_user: str, lndb_password: str, python_version: str = "3.10"
) -> None:
    """Uploads all ontology file artifacts to the specified instance.

    Uses all files generated by nox that are found in the _dynamic folder.

    Args:
        instance: The lndb instance to upload the files to.
        lndb_user: The lndb username.
        lndb_password: The associated password of the lndb user.
        python_version: The Python version that ran nox. Defaults to '3.10'.
    """
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


_upload_ontology_artifacts(
    instance="bionty-assets",
    lndb_user="testuser2@lamin.ai",
    lndb_password="goeoNJKE61ygbz1vhaCVynGERaRrlviPBVQsjkhz",
    python_version="3.9",
)
