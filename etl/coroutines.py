import logging
from functools import wraps

from kafka import OffsetAndMetadata, TopicPartition


def coroutine(func):
    @wraps(func)
    def inner(*args, **kwargs):
        fn = func(*args, **kwargs)
        next(fn)
        return fn

    return inner


@coroutine
def consume_film_views_from_kafka(consumer, target):
    while True:
        logging.info("Starting to consume from kafka")
        for message in consumer:
            target.send((message.offset, message.partition, message.key, message.value))


@coroutine
def transform_view_data(target):
    while data := (yield):
        offset, partition, key, value = data
        # to-do: transform here
        target.send((offset, partition, value))


@coroutine
def write_to_clickhouse(consumer, topic):
    while data := (yield):
        offset, partition, view_event = data
        # to-do: write to clickhouse
        topic_partition = TopicPartition(topic, partition)
        options = {topic_partition: OffsetAndMetadata(offset + 1, None)}
        consumer.commit(options)
