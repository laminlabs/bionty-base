from bionty.dev._handle_sources import parse_sources_yaml

"""
2. If ontology is reachable -> get latest version
3. Compare -> create some result -> throw error if some found
4. Create CI job that runs this script
"""

sources = parse_sources_yaml()
latest_versions = (
    sources.groupby("source")["version"]
    .apply(
        lambda version: version.iloc[
            version.astype(str).str.replace(".", "").str.isdigit().argmax()
        ]
    )
    .reset_index()
)
latest_versions_dict = latest_versions.set_index("source")["version"].to_dict()

for ontology, version in latest_versions_dict.items():
    pass

# def check_mondo_ontology_version():
#     # Retrieve the MONDO ontology entry from BioRegistry
#     mondo_version = bioregistry.get_version("mondo")
#     if     mondo_version:
#         if mondo_version:
#             print(f"Latest version of MONDO ontology: {mondo_version}")
#         else:
#             print("Version information not found for MONDO ontology.")
#     else:
#         print("Failed to retrieve MONDO ontology entry from BioRegistry.")
#
# # Call the function to check the MONDO ontology version
# check_mondo_ontology_version()
