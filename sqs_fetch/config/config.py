import yaml


def load_config(config_path: str) -> dict:
    """
    This function loads the config file and returns it as a dictionary.
    :param config_path:
    :return:
    """

    with open(config_path, 'r') as file:
        return yaml.safe_load(file)
