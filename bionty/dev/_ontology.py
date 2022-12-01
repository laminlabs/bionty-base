import requests  # type: ignore


def ontology_info(namespace: str) -> dict:
    """Get the latest information of an ontology from OLS.

    Args:
        namespace: ontology namespace (e.g: cl, efo, go)
    """
    headers = {"Accept": "application/json"}
    r = requests.get(
        f"http://www.ebi.ac.uk/ols/api/ontologies/{namespace.lower()}", headers=headers
    )

    if r.status_code != 200:
        raise RuntimeError(f"No information found about ontology {namespace}.")

    return r.json().get("config")
