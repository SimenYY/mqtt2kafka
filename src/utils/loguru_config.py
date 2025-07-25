#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:FileName: log.py
:Project:
:Brand:
:Version:
:Description:
:Author: He Yinyu
:Link:
:Time: 2025/4/22 16:32
"""
import sys
import logging
from pathlib import Path
import inspect

import loguru


class InterceptHandler(logging.Handler):
    """
    使用：logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    """

    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = loguru.logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        loguru.logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class LoguruConfig:
    """配置loguru

    注释：
        1. 能够添加拦截原生的logger
        2. 能够配置console和file两种常用输出
    
    Settings:
        log_level: str = "DEBUG"
        log_dir: str = "logs"
        log_rotation: str = "00:00"
        log_retention: str = "3 days"
        log_compression: str = "zip"
        log_enqueue: bool = True
    
    """

    def __init__(self, name: str, level: str = "DEBUG"):
        loguru.logger.remove()

        self.name = name
        self.level = level

    def include_logging_namespace(self, namespace: str) -> None:
        """
        添加logging命名空间
        """
        logging_logger = logging.getLogger(namespace)
        self.include_logging_logger(logging_logger)

    def include_logging_logger(self, logging_logger: logging.Logger) -> None:
        """
        添加logging.logger
        """
        logging_logger.setLevel(self.level)
        logging_logger.handlers.clear()
        logging_logger.addHandler(InterceptHandler())
        logging_logger.propagate = False

    def setup_console(self) -> None:
        """控制台输出
        
        Settings:
            log_level: str = "DEBUG"
        
        """
        loguru.logger.add(
            sys.stdout,
            level=self.level
        )

    def setup_file(
            self,
            log_dir: str = 'logs',
            *,
            rotation: str = '00:00',
            retention: str = '3 days',
            compression: str = 'zip',
            enqueue: bool = True,
    ):
        """文件输出
        
        Settings:
            log_dir: str = "logs"
            log_rotation: str = "00:00"
            log_retention: str = "3 days"
            log_compression: str = "zip"
            log_enqueue: bool = True
        
        :param str log_dir: _description_, defaults to 'logs'
        :param str log_rotation: _description_, defaults to "00:00"
        :param str log_retention: _description_, defaults to "3 days"

        :param str log_dir: _description_, defaults to 'logs'
        :param _type_ rotation: _description_, defaults to '00:00'
        :param str retention: _description_, defaults to '3 days'
        :param str compression: _description_, defaults to 'zip'
        :param bool enqueue: _description_, defaults to True
        """
        _log_dir = Path(log_dir)
        _log_dir.mkdir(parents=True, exist_ok=True)
        log_file = _log_dir / self.name / (f"{self.name}" + "_{time: YYYY-MM-DD}.log")
        loguru.logger.add(
            str(log_file),
            level=self.level,
            rotation=rotation,
            retention=retention,
            compression=compression,
            enqueue=enqueue
        )


__all__ = ["LoguruConfig", "InterceptHandler"]