from src.mqtt2kafka import Mqtt2Kafka
from src import logger
from src.utils.loguru_config import LoguruConfig
from src.settings import settings
from src.utils.singleton import SingleAppGuard

lc = LoguruConfig(settings.app_title, settings.log_level)
lc.include_logging_logger(logger)
lc.setup_console()
lc.setup_file(
    settings.log_dir,
    rotation=settings.log_rotation,
    retention=settings.log_retention,
    compression=settings.log_compression,
    enqueue=settings.log_enqueue,
)

def art_print():
    from art import tprint
    
    tprint(settings.app_title)
    print(f"{settings.app_title} v{settings.app_version}")
    print()
    print(".exe同目录下配置文件: config.yaml")
    print()
def main():
        try:
            mqtt_2_kafka = Mqtt2Kafka()
            mqtt_2_kafka.run()
        except Exception as e:
            logger.exception(e)
    
if __name__ == "__main__":
    # pyinstaller -F .\main.py -n mqtt2kafka
    art_print()
    
    with SingleAppGuard(app_name=settings.app_title):
        main()