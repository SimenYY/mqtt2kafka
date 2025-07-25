import logging

from src.kafka_client  import KafkaProducer
from src.mqtt_client import MqttClientV2
from src.settings import settings

logger = logging.getLogger(__name__)

class Mqtt2Kafka:
    def __init__(self) -> None:
        self.kafka_producer = KafkaProducer(
            bootstrap_servers=",".join(settings.kafka_servers),
        )
        
        self.mqtt_client = MqttClientV2(
            settings.mqtt_host, 
            settings.mqtt_port, 
        )
        self.mqtt_client.set_on_connect(self.on_mqtt_connect)
        self.mqtt_client.set_on_message(self.on_mqtt_message)
        self.mqtt_client.set_on_disconnect()
        self.mqtt_client.set_on_subscribe()
        self.mqtt_client.connect()
    
    def on_mqtt_message(self, client, userdata, message):
        logger.debug(f'Received "{message.payload}" from "{message.topic}" topic')
        self.kafka_producer.produce(self.escape_topic(message.topic), message.payload)
        self.kafka_producer.producer.poll(0)

    def on_mqtt_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            logger.error(f'Failed to connect MQTT broker[{self.mqtt_client.address}], reason code: {reason_code}.')
        else:
            logger.info(f'Connected to MQTT Broker[{self.mqtt_client.address}], client id: {self.mqtt_client.client_id}.')
            for topic in settings.mqtt_topic_list:
                self.mqtt_client.subscribe(topic)
    
    def escape_topic(self, topic: str) -> str:
        escaped = topic
        
        if "/" in escaped:
            escaped = escaped.replace("/", "_")
        
        if escaped.startswith("_"):
            escaped = escaped[1:]
        
        return escaped
    
    def run(self):
        if not isinstance(self.mqtt_client, MqttClientV2):
            raise RuntimeError("MQTT Client is not initialized.")
        self.mqtt_client.run()