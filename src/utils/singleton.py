#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:FileName: singleInstance.py
:Project:
:Brand:
:Version:
:Description: 
:Author: He YinYu
:Link:
:Time: 2025/4/1 14:07
"""

import sys
from pathlib import Path
import logging
from dataclasses import dataclass
from filelock import FileLock


logger = logging.getLogger(__name__)

@dataclass
class SingleAppGuard:
    """应用二次启动文件锁

    Usage:
        with SingleAppGuard():
            print("your func")

    """
    app_name: str = "app.lock"

    def __post_init__(self) -> None:
        lock_file = Path.cwd() / f"{self.app_name}.lock"
        self.lock = FileLock(lock_file)
        logger.info(f"lock file path: {str(lock_file)}")
    def __enter__(self):
        try:
            self.lock.acquire(timeout=0)
            logger.info("The program is started successfully")
        except TimeoutError:
            logger.warning("The program is already running")
            sys.exit(0)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.lock.release()
        logger.info("The program is exited successfully")

        if exc_type is not None:
            logger.error(f"Exception in context: {exc_val}")