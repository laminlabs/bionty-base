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
species: `name` of `Species` entity.
        source: The key of the source in the local.yml versions file.
                  Get all available databases with `bionty.display_available_sources`.
        version: The version of the ontology. Typically a date or an actual version.
                  Get available versions with `bionty.display_available_sources`.
"""
species_removed_tmp = "\n".join(doc_entites.split("\n")[1:]).split("\n")
species_removed_tmp[0] = remove_prefix(species_removed_tmp[0], "        ")
species_removed = "\n".join(species_removed_tmp)


doc_curate = """\
df: DataFrame with a column of identifiers
        column: If `column` is `None`, checks the existing index for compliance with
                  the default identifier.
                If `column` denotes an entity identifier, tries to map that identifier
                  to the default identifier.
        reference_id: The type of identifier for mapping.
"""
