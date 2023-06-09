import os
import tempfile

import pytest

from bionty.dev._handle_sources import (
    add_records_to_existing_dict,
    parse_currently_used_sources,
    parse_sources_yaml,
    records_diff_btw_yamls,
)
from bionty.dev._io import load_yaml


@pytest.fixture(scope="function")
def versions_yaml_replica():
    input_file_content = """
    version: "0.2.0"
    Species:
      ensembl:
        all:
          release-108:
            source: https://ftp.ensembl.org/pub/release-108/species_EnsemblVertebrates.txt
        name: Ensembl
        website: https://www.ensembl.org/index.html
    Gene:
      ensembl:
        human:
          release-108:
            source: https://ftp.ensembl.org/pub/release-108/mysql/homo_sapiens_core_108_38/
          release-107:
            source: https://ftp.ensembl.org/pub/release-107/mysql/homo_sapiens_core_107_38/
        mouse:
          release-108:
            source: https://ftp.ensembl.org/pub/release-108/mysql/mus_musculus_core_108_39/
        name: Ensembl
        website: https://www.ensembl.org/index.html
    CellType:
      cl:
        name: Cell Ontology
        website: https://obophenotype.github.io/cell-ontology/
        all:
          2023-02-15:
            source: http://purl.obolibrary.org/obo/cl/releases/2023-02-15/cl-base.owl
            md5: 9331a6a029cb1863bd0584ab41508df7
          2022-08-16:
            source: http://purl.obolibrary.org/obo/cl/releases/2022-08-16/cl.owl
            md5: d0655766574e63f3fe5ed56d3c030880
    """
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        f.write(input_file_content)
        f.flush()
        yield f.name

    os.unlink(f.name)


@pytest.fixture(scope="function")
def new_versions_yaml_replica():
    input_file_content = """
    version: "0.2.0"
    Species:
      ensembl:
        all:
          release-108:
            source: https://ftp.ensembl.org/pub/release-108/species_EnsemblVertebrates.txt
        name: Ensembl
        website: https://www.ensembl.org/index.html
        new-species:
          release-x:
            source: new-species-source-link
    Gene:
      ensembl:
        human:
          release-108:
            source: https://ftp.ensembl.org/pub/release-108/mysql/homo_sapiens_core_108_38/
          release-107:
            source: https://ftp.ensembl.org/pub/release-107/mysql/homo_sapiens_core_107_38/
        mouse:
          release-108:
            source: https://ftp.ensembl.org/pub/release-108/mysql/mus_musculus_core_108_39/
        name: Ensembl
        website: https://www.ensembl.org/index.html
      new-source:
        human:
          release-x:
            source: new-gene-source-link
    CellType:
      cl:
        name: Cell Ontology
        website: https://obophenotype.github.io/cell-ontology/
        all:
          new-version:
            source: new-cell-type-source
            md5: new-md5
          2023-02-15:
            source: http://purl.obolibrary.org/obo/cl/releases/2023-02-15/cl-base.owl
            md5: 9331a6a029cb1863bd0584ab41508df7
          2022-08-16:
            source: http://purl.obolibrary.org/obo/cl/releases/2022-08-16/cl.owl
            md5: d0655766574e63f3fe5ed56d3c030880
    """
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        f.write(input_file_content)
        f.flush()
        yield f.name

    os.unlink(f.name)


@pytest.fixture(scope="function")
def current_yaml_replica():
    input_file_content = """
    Species:
      all:
        ensembl: release-108
    """
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        f.write(input_file_content)
        f.flush()
        yield f.name

    os.unlink(f.name)


def test_parse_versions_yaml(versions_yaml_replica):
    parsed_df = parse_sources_yaml(versions_yaml_replica)
    assert parsed_df.shape == (6, 8)
    assert all(
        parsed_df["entity"].values
        == ["Species", "Gene", "Gene", "Gene", "CellType", "CellType"]
    )
    assert all(
        parsed_df["species"].values == ["all", "human", "human", "mouse", "all", "all"]
    )
    assert all(
        parsed_df["source_key"].values
        == ["ensembl", "ensembl", "ensembl", "ensembl", "cl", "cl"]
    )


def test_parse_current_versions(versions_yaml_replica):
    expected = {
        "Species": {"all": {"ensembl": "release-108"}},
        "Gene": {
            "human": {"ensembl": "release-108"},
            "mouse": {"ensembl": "release-108"},
        },
        "CellType": {"all": {"cl": "2023-02-15"}},
    }

    assert parse_currently_used_sources(versions_yaml_replica) == expected


def test_add_records_to_existing_dict(new_versions_yaml_replica, versions_yaml_replica):
    expected = [
        {
            "entity": "Species",
            "source_key": "ensembl",
            "species": "new-species",
            "version": "release-x",
            "url": "new-species-source-link",
            "md5": "",
            "source_name": "Ensembl",
            "source_website": "https://www.ensembl.org/index.html",
        },
        {
            "entity": "Gene",
            "source_key": "new-source",
            "species": "human",
            "version": "release-x",
            "url": "new-gene-source-link",
            "md5": "",
            "source_name": "",
            "source_website": "",
        },
        {
            "entity": "CellType",
            "source_key": "cl",
            "species": "all",
            "version": "new-version",
            "url": "new-cell-type-source",
            "md5": "new-md5",
            "source_name": "Cell Ontology",
            "source_website": "https://obophenotype.github.io/cell-ontology/",
        },
    ]

    records = records_diff_btw_yamls(new_versions_yaml_replica, versions_yaml_replica)

    assert records == expected

    updated_dict = add_records_to_existing_dict(
        records, load_yaml(versions_yaml_replica)
    )
    assert updated_dict.get("Species").get("ensembl").get("new-species").get(
        "release-x"
    ) == {"source": "new-species-source-link", "md5": ""}
    assert updated_dict.get("Gene").get("new-source").get("human").get("release-x") == {
        "source": "new-gene-source-link",
        "md5": "",
    }
    assert updated_dict.get("CellType").get("cl").get("all").get("new-version") == {
        "source": "new-cell-type-source",
        "md5": "new-md5",
    }
