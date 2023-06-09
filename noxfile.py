import os
import shutil
import sys

import nox
from laminci import upload_docs_artifact
from laminci.nox import build_docs, login_testuser1, run_pre_commit

nox.options.default_venv_backend = "none"


@nox.session
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session
@nox.parametrize("group", ["bionty-unit", "bionty-docs", "lnschema-bionty"])
def build(session, group):
    session.run(*"pip install .[dev,test]".split())
    coverage_args = "--cov=bionty --cov-append --cov-report=term-missing"  # noqa
    if group == "bionty-unit":
        session.run(*f"pytest -s {coverage_args} ./tests".split())
    elif group == "bionty-docs":
        session.run(*f"pytest -s {coverage_args} ./docs/guide".split())
        shutil.copy("README.md", "docs/README.md")
        build_docs(session)
        upload_docs_artifact(aws=True)
    else:
        # navigate into submodule so that lamin-project.yml is correctly read
        os.chdir("./lnschema-bionty")
        session.run(*"pip install .[test]".split())
        session.run(*"git clone https://github.com/laminlabs/lamindb --depth 1".split())
        if sys.platform.startswith("linux"):  # remove version pin when running on CI
            session.run(*"sed -i /lnschema_bionty/d ./lamindb/pyproject.toml".split())
        session.run(*"pip install ./lamindb".split())
        login_testuser1(session)
        session.run(
            "lamin",
            "init",
            "--storage",
            "./docs/guide/lnbionty-test",
            "--schema",
            "bionty",
        )
        session.run("pytest", "-s", "./tests", "--ignore", "./tests/test_migrations.py")
