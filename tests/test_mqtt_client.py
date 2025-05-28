from app.mqtt_client import MqttClientV2, logger
from app.utils.loguru_config import InterceptHandler
from app.settings import settings
logger.addHandler(InterceptHandler())
logger.setLevel("DEBUG")

mqtt_client = MqttClientV2(settings.mqtt_host)
mqtt_client.set_on_connect()
mqtt_client.set_on_disconnect()
mqtt_client.set_on_subscribe()
mqtt_client.set_on_publish()

mqtt_client.connect()

mqtt_client.run()