import nox
from laminci import move_built_docs_to_docs_slash_project_slug
from laminci.nox import build_docs, run_pre_commit

nox.options.default_venv_backend = "none"


@nox.session
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session
def docs(session: nox.Session):
    build_docs(session, strict=True)


@nox.session
@nox.parametrize("group", ["bionty-unit", "bionty-docs"])
def build(session: nox.Session, group: str):
    session.run(*"uv pip install --system -e .[dev]".split())
    coverage_args = "--cov=bionty_base --cov-append --cov-report=term-missing"
    if group == "bionty-unit":
        session.run(*f"pytest {coverage_args} ./tests".split())
    elif group == "bionty-docs":
        session.run(*f"pytest -s {coverage_args} ./docs/guide".split())
        docs(session)
        move_built_docs_to_docs_slash_project_slug()
