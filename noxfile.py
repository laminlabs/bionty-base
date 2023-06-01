import os
import sys

import nox
from laminci import move_built_docs_to_docs_slash_project_slug, upload_docs_artifact
from laminci.nox import build_docs, login_testuser1, run_pre_commit, run_pytest

nox.options.default_venv_backend = "none"


@nox.session
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session
@nox.parametrize("package", ["bionty", "lnschema-bionty"])
def build(session, package):
    session.run(*"pip install .[dev,test]".split())
    if package == "bionty":
        run_pytest(session)
        build_docs(session)
        upload_docs_artifact(aws=True)
        move_built_docs_to_docs_slash_project_slug()
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
