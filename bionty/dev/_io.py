import yaml  # type:ignore


def load_yaml(filename: str):
    with open(filename, "r") as f:
        return yaml.safe_load(f)


def write_yaml(data: dict, filename: str):
    with open(filename, "w") as f:
        yaml.dump(data, f)
