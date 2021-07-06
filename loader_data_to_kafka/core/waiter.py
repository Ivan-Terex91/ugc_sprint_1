import asyncio
import logging

import config
from aiokafka import AIOKafkaProducer
from kafka.errors import KafkaConnectionError

logger = logging.getLogger(__name__)


async def wait_for_kafka():
    kafka_status = 0
    while not kafka_status:
        try:
            kafka_inst = AIOKafkaProducer(bootstrap_servers=config.KAFKA_DSN)
            await kafka_inst.start()
            await kafka_inst.stop()
            kafka_status = 1
        except KafkaConnectionError as exc:
            logger.error(exc)
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(wait_for_kafka())
