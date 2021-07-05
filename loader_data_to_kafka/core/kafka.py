import json

from aiokafka import AIOKafkaProducer

kafka_producer: AIOKafkaProducer = None


async def get_kafka_producer() -> AIOKafkaProducer:
    return kafka_producer


class KafkaProducer:
    def __init__(self, kafka_producer: AIOKafkaProducer):
        self.kafka_producer = kafka_producer

    async def send_data(self, msg, topic):
        await self.kafka_producer.send(topic=topic, value=json.dumps(msg))
