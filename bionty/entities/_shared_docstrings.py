from textwrap import dedent


def _doc_params(**kwds):  # pragma: no cover
    """\
    Docstrings should start with "\" in the first line for proper formatting.
    """

    def dec(obj):
        obj.__orig_doc__ = obj.__doc__
        obj.__doc__ = dedent(obj.__doc__).format_map(kwds)
        return obj

    return dec


def remove_prefix(
    text, prefix
):  # pragma: no cover  # TODO replace with removeprefix Python 3.9+
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text


doc_entites = """\
species: `name` of `Species` entity Entity.
        id: Field name that should constitute the primary reference for each value.
            It will also be the primary key in the corresponding SQL Entity.
        database: The key of the database in the local.yml versions file.
                  Get all available databases with `bionty.display_available_versions`.
        version: The version of the ontology. Typically a date or an actual version.
                  Get available versions with `bionty.display_available_versions`.
"""
species_removed_tmp = "\n".join(doc_entites.split("\n")[1:]).split("\n")
species_removed_tmp[0] = remove_prefix(species_removed_tmp[0], "        ")
species_removed = "\n".join(species_removed_tmp)
