"""
自动化构建脚本，用于Workflow
"""
import subprocess

build_command = [
    "pyinstaller",
    "main.py",
    "-F",                  # 单文件
    "-n", "mqtt2kafka"        # 输出文件名
]
subprocess.run(build_command)