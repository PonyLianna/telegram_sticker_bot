class ConfigurationMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


import yaml


class Configuration(metaclass=ConfigurationMeta):
    def __init__(self):
        self.data = {}
        self.get_config()

    def get_config(self, path="./config.yaml"):
        with open(path) as f:
            self.data = yaml.load(f, Loader=yaml.SafeLoader)
