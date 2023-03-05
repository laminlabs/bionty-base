import inspect
from textwrap import dedent
from typing import Callable, Optional, Union


def getdoc(c_or_f: Union[Callable, type]) -> Optional[str]:  # pragma: no cover
    if getattr(c_or_f, "__doc__", None) is None:
        return None
    doc = inspect.getdoc(c_or_f)
    if isinstance(c_or_f, type) and hasattr(c_or_f, "__init__"):
        sig = inspect.signature(c_or_f.__init__)  # type: ignore
    else:
        sig = inspect.signature(c_or_f)

    def type_doc(name: str):
        param: inspect.Parameter = sig.parameters[name]
        cls = getattr(param.annotation, "__qualname__", repr(param.annotation))
        if param.default is not param.empty:
            return f"{cls}, optional (default: {param.default!r})"
        else:
            return cls

    return "\n".join(
        f"{line} : {type_doc(line)}" if line.strip() in sig.parameters else line
        for line in doc.split("\n")
    )


def _doc_params(**kwds):  # pragma: no cover
    """\
    Docstrings should start with "\" in the first line for proper formatting.
    """

    def dec(obj):
        obj.__orig_doc__ = obj.__doc__
        obj.__doc__ = dedent(obj.__doc__).format_map(kwds)
        return obj

    return dec


doc_entites = """\
species: `name` of `Species` entity Entity.
        id: Ontology ID
        database: Ontology database.
        version: Ontology version.
"""
