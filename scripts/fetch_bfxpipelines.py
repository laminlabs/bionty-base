import json
import os

from github import Github

gh_login = Github(os.getenv("GITHUB_TOKEN"))
nf_core_org = gh_login.get_organization("nf-core")

blacklist = ["cookiecutter", "tools"]

nf_core_pipelines = []
for repo in nf_core_org.get_repos():
    if "pipeline" in [topic for topic in repo.get_topics()]:
        repo_info = {
            "name": repo.name,
            "versions": [release.tag_name for release in repo.get_releases()],
            "url": repo.url,
        }
        if repo_info["name"] in blacklist:
            continue
        if len(repo_info["versions"]) < 1:
            repo_info["versions"] = "pre-release"

        nf_core_pipelines.append(repo_info)

with open("nf_core_pipelines_info.json", "w") as f:
    json_data = json.dumps(nf_core_pipelines, indent=4)
    f.write(json_data)
