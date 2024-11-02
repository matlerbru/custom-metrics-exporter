import logging
import os
import typing

import pydantic
import yaml


class NoConfigurationError(BaseException):
    pass


class DirectoryUsage(pydantic.BaseModel):
    host: str
    username: str
    password: str
    path: str

    @pydantic.model_validator(mode="before")
    def set_credentials(cls, values):
        if values.get("username") is None:
            values["username"] = os.getenv(f"{values['host'].upper()}_USERNAME")
        if values.get("password") is None:
            values["password"] = os.getenv(f"{values['host'].upper()}_PASSWORD")
        return values


class Config(pydantic.BaseModel):
    scrape_interval: int = 60
    directory_usage: list[DirectoryUsage]


def config_loader(paths: list[str]) -> Config:
    for path in paths:
        try:
            with open(path, "r") as stream:
                parsed_yaml = typing.cast(dict, yaml.safe_load(stream))
                logging.info(f"Loading configfile: {path}")
                return Config.model_validate(parsed_yaml)
        except yaml.scanner.ScannerError as e:
            logging.error(f"Unable to parse file {path}: {str(e)}.")
        except FileNotFoundError:
            pass
    else:
        raise Exception("Not able to load configfile.")


config = config_loader(["config.yaml", "/modbus-to-mqtt/config.yaml"])
