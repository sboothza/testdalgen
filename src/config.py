from base.config_base import ConfigBase


class Config(ConfigBase):
    def __init__(self, connection_string: str = ""):
        super().__init__(connection_string)
