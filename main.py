from art  import text2art


from app.mqtt2kafka import Mqtt2Kafka
from app import logger
from app.utils.loguru_config import LoguruConfig
from app.settings import settings
from app.utils.singleton import SingleAppGuard

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

def ahead_print():
    print(text2art(settings.app_title))
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
    ahead_print()
    
    with SingleAppGuard(app_name=settings.app_title):
        main()