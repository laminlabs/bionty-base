import glob
import json
import os
import random
import string
from typing import Dict

from github import Github
from rich.progress import track

BASE_BFX_PIPELINES_PATH = "bionty/versions/bfxpipelines_data"


def generate_base62_string(full_pipeline_name: str) -> str:
    """Generates a 9 char base62 ID for a pipeline name.

    Args:
        full_pipeline_name: The full pipeline name. Expected to be the actual pipeline name with potential spaces.

    Returns:
        A 9 char ID.
    """
    alphabet = string.ascii_letters + string.digits
    random.seed(full_pipeline_name)
    base62_string = ""
    for _ in range(9):
        base62_string += random.choice(alphabet)

    return base62_string


def generate_nf_core_pipelines_info() -> None:
    """Generates a json file that contains all required pipelines information by querying the nf-core Github org."""
    gh_login = Github(os.getenv("GITHUB_TOKEN"))
    nf_core_org = gh_login.get_organization("nf-core")
    blacklist = ["cookiecutter", "tools"]
    nf_core_pipelines = {}
    for repo in track(
        nf_core_org.get_repos(),
        description="Fetching information from nf-core repositories...",
    ):
        if "pipeline" in [topic for topic in repo.get_topics()]:
            if repo.name in blacklist:
                continue

            for version in repo.get_releases():
                actual_version = (
                    version.tag_name if len(version.tag_name) >= 1 else "pre-release"
                )
                pipeline_name = f"{repo.name} v{actual_version}"
                underscore_pipeline_name = (
                    pipeline_name.replace(" ", "_").replace(".", "_").replace("-", "_")
                )

                nf_core_pipelines[underscore_pipeline_name] = {
                    "id": generate_base62_string(pipeline_name),
                    "name": pipeline_name,
                    "versions": actual_version,
                    "reference": repo.url,
                }

    with open(f"{BASE_BFX_PIPELINES_PATH}/nf_core_pipelines_info.json", "w") as f:
        json_data = json.dumps(nf_core_pipelines, indent=4)
        f.write(json_data)


def merge_json_files(pipelines_folder_path: str, output_path: str) -> None:
    """Merge all JSON files in a folder and write the merged data to a new JSON file.

    Args:
        pipelines_folder_path: Path to the folder containing the JSON files.
        output_path: Path to the output JSON file.
    """
    file_paths = glob.glob(pipelines_folder_path + "/*.json")

    pipeline_json: Dict = {}

    for file_path in file_paths:
        with open(file_path, "r") as f:
            if not file_path.endswith("pipelines.json"):
                pipelines_info = json.load(f)
                pipeline_json = {**pipeline_json, **pipelines_info}

    with open(output_path, "w") as f:
        json.dump(pipeline_json, f, indent=4)


generate_nf_core_pipelines_info()
merge_json_files(
    pipelines_folder_path=BASE_BFX_PIPELINES_PATH,
    output_path=f"{BASE_BFX_PIPELINES_PATH}/bfxpipelines.json",
)
