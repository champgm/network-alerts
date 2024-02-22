from pathlib import Path
from pydantic import BaseModel
from typing import List
import yaml


class MonitoringConfig(BaseModel):
    target_ip: str
    check_interval: int
    failures_allowed: int


class LoggingConfig(BaseModel):
    file_path: str
    level: str


class GoogleTokenConfig(BaseModel):
    grant_type: str
    refresh_token: str
    client_id: str
    client_secret: str


class EmailConfig(BaseModel):
    google_token: GoogleTokenConfig
    sender: str
    recipients: List[str]


class Config(BaseModel):
    monitoring: MonitoringConfig
    logging: LoggingConfig
    email: EmailConfig


def get_config() -> Config:
    current_file_directory = Path(__file__).parent
    config_path = current_file_directory / "../configuration.yaml"
    with open(config_path, "r") as file:
        data = yaml.safe_load(file)
        return Config(**data)
