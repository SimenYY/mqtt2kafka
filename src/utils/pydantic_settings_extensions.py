#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:FileName: pydantic_settings_extensions.py
:Project:
:Brand:
:Version:
:Description: 
:Author: He YinYu
:Link:
:Time: 2025/5/16 23:40
"""
from pathlib import Path

from pydantic_settings import SettingsConfigDict
from pydantic_settings import (
    BaseSettings,
    YamlConfigSettingsSource,
    JsonConfigSettingsSource,
    PydanticBaseSettingsSource,
) 


class ExtendedBaseSettings(BaseSettings):

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        sources = super().settings_customise_sources(
            settings_cls,
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )
        yaml_settings = YamlConfigSettingsSource(
            cls,
            yaml_file=cls.model_config.get("yaml_file", Path("")),
            yaml_file_encoding=cls.model_config.get("yaml_file_encoding", None)
        )
        json_settings = JsonConfigSettingsSource(
            cls,
            json_file=cls.model_config.get("json_file", Path("")),
            json_file_encoding=cls.model_config.get("json_file_encoding", None)
        )
        return (yaml_settings, json_settings) + sources


class YamlSettings(ExtendedBaseSettings):
        model_config = SettingsConfigDict(
        yaml_file="config.yaml",
        yaml_file_encoding="utf-8",
        extra='ignore',
        case_sensitive=True,
    )


class JsonSettings(ExtendedBaseSettings):
        model_config = SettingsConfigDict(
        json_file="config.json",
        json_file_encoding="utf-8",
        extra='ignore',
        case_sensitive=True,
    )
        
__all__ = ["YamlSettings", "JsonSettings"]