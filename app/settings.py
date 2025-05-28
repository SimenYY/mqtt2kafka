from pathlib import Path
from typing import Optional, List

from app.utils.pydantic_settings_extensions import YamlSettings

APP_DIR = Path(__file__).resolve().parent



class Settings(YamlSettings):
    
    app_title: str = "Mqtt2Kafka"
    app_version: str = "0.1.0"
    
    encoding: str = "utf-8"
    
    # mqtt settings
    mqtt_host: str = "localhost"
    mqtt_port: int = 1883
    mqtt_topic_list: List[str] = []
    
    # kafka settings
    kafka_servers: List[str] = ["localhost:9092"]
    
    # log settings
    log_level: str = "DEBUG"
    log_dir: str = "logs"
    log_rotation: str = "00:00"
    log_retention: str = "3 days"
    log_compression: str = "zip"
    log_enqueue: bool = True
    
settings = Settings()