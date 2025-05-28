from app.kafka_client import KafkaProducer

producer = KafkaProducer()
print(producer.bootstrap_servers)