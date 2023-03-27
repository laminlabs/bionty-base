import os

import nox
from laminci import move_built_docs_to_docs_slash_project_slug, upload_docs_dir
from laminci.db import setup_local_test_postgres
from laminci.nox import build_docs, login_testuser1, run_pre_commit, run_pytest

nox.options.reuse_existing_virtualenvs = True


@nox.session(python=["3.8", "3.9", "3.10", "3.11"])
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session
@nox.parametrize("package", ["bionty", "lnschema-bionty"])
def build(session, package):
    login_testuser1(session)
    session.install(".[dev,test]")
    session.install("./lnschema-bionty[dev,test]")
    if package == "bionty":
        run_pytest(session)
        build_docs(session)
        upload_docs_dir()
        move_built_docs_to_docs_slash_project_slug()
    else:
        # navigate into submodule so that lamin-project.yml is correctly read
        os.chdir("./lnschema-bionty")
        # init a postgres instance
        pgurl = setup_local_test_postgres()
        init_instance = f"lamin init --storage pgtest --db {pgurl} --schema bionty"
        session.run(*init_instance.split(" "), external=True)
        session.run("pytest", "-s", "./tests")
