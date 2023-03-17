from bionty._settings import settings
from bionty.dev._io import load_yaml, write_yaml

_LOCAL_PATH = settings.versionsdir / "local.yaml"


def update_yaml_from_unversionized_to_0_1() -> None:
    """Update an old YAML format (unversionized) to version 0.1.

    Args:
        old_yaml: The unversionized yaml.
    """
    old_yaml = load_yaml(_LOCAL_PATH)
    new_yaml = {}

    new_yaml["version"] = "0.1.0"

    for entities, values in old_yaml.items():
        new_values = {}

        for sub_section, sub_values in values.items():
            new_sub_values = {}

            if "versions" in sub_values:
                new_versions = {}

                for version, url in sub_values["versions"].items():
                    new_versions[version] = [url, ""]

                new_sub_values["versions"] = new_versions

                for key, value in sub_values.items():
                    if key != "versions":
                        new_sub_values[key] = value
            else:
                new_sub_values = sub_values
            new_values[sub_section] = new_sub_values
        new_yaml[entities] = new_values  # type: ignore

    write_yaml(new_yaml, _LOCAL_PATH, sort_keys=False, default_flow_style=False)
