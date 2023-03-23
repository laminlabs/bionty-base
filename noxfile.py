import nox
from laminci import move_built_docs_to_docs_slash_project_slug, upload_docs_dir
from laminci.nox import (
    build_docs,
    login_testuser1,
    run_pre_commit,
    run_pytest,
    setup_test_instances_from_main_branch,
)

nox.options.reuse_existing_virtualenvs = True


@nox.session(python=["3.8", "3.9", "3.10", "3.11"])
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session
@nox.parametrize("package", ["bionty", "lnschema-bionty"])
def build(session, package):
    login_testuser1(session)
    setup_test_instances_from_main_branch(session)
    session.install(".[dev,test]")
    session.install("./lnschema-bionty[dev,test]")
    if package == "bionty":
        run_pytest(session)
        build_docs(session)
        upload_docs_dir()
        move_built_docs_to_docs_slash_project_slug()
    else:
        session.run("pytest", "-s", "./lnschema-bionty/tests")
