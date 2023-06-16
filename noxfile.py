import shutil

import nox
from laminci import upload_docs_artifact
from laminci.nox import build_docs, run_pre_commit

nox.options.default_venv_backend = "none"


@nox.session
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session
@nox.parametrize("group", ["bionty-unit", "bionty-docs"])
def build(session, group):
    session.run(*"pip install -e .[dev]".split())
    coverage_args = "--cov=bionty --cov-append --cov-report=term-missing"  # noqa
    if group == "bionty-unit":
        session.run(*f"pytest {coverage_args} ./tests".split())
    elif group == "bionty-docs":
        session.run(*f"pytest -s {coverage_args} ./docs/guide".split())
        shutil.copy("README.md", "docs/README.md")
        build_docs(session)
        upload_docs_artifact(aws=True)
