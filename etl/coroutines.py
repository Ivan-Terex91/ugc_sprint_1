import logging
import coloredlogs

from functools import wraps
from collections import deque
from kafka import OffsetAndMetadata, TopicPartition

from datetime import datetime
import dateutil.parser

import json

import backoff

logger = logging.getLogger("ETL")

coloredlogs.install(level="DEBUG", logger=logger)


@backoff.on_exception(backoff.expo, Exception)
def insert_clickhouse(db, values):
    db.execute("INSERT INTO default.views (user_id, movie_id, viewing_progress, viewing_date) VALUES", values)
    logger.info("data delivered in clickhouse")


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
        logger.info("Starting to consume from kafka")
        for message in consumer:
            target.send((message.offset, message.partition, message.key, message.value))
            logger.info(
                '\n'
                f'    offset: {message.offset}\n'
                f"    partition: {message.partition}\n"
                f"    key: {message.key}\n"
                f"    value: {json.loads(message.value.decode())}\n"
            )


@coroutine
def transform_view_data(target):
    while data := (yield):
        offset, partition, key, value = data
        value = json.loads(value.decode())
        value['viewing_date'] = dateutil.parser.parse(value['viewing_date'])
        target.send((offset, partition, value))


@coroutine
def buffer_data(target, size_buffer=1000):
    part = deque()
    while data := (yield):
        offset, partition, view_event = data
        part.append(view_event)
        if len(part) >= size_buffer:
            target.send((offset, partition, list(part)))
            part.clear()


@coroutine
def write_to_clickhouse(consumer, topic, db):
    while data := (yield):
        offset, partition, view_event = data
        insert_clickhouse(db, view_event)
        topic_partition = TopicPartition(topic, partition)
        options = {topic_partition: OffsetAndMetadata(offset + 1, None)}
        consumer.commit(options)
