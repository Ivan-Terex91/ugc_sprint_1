import os

from clickhouse_driver import Client
from coroutines import (buffer_data, consume_film_views_from_kafka,
                        transform_view_data, write_to_clickhouse)
from kafka import KafkaConsumer

if __name__ == "__main__":
    consumer = KafkaConsumer(
        os.getenv("MOVIE_VIEWS_TOPIC"),
        bootstrap_servers=[os.getenv("BOOTSTRAP_SERVER")],
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        group_id="kafka-to-clickhouse",
        api_version=(0, 10, 1),
    )
    db = Client(host="clickhouse-node1")

    writer_sink = write_to_clickhouse(consumer, os.getenv("MOVIE_VIEWS_TOPIC"), db)
    buffer = buffer_data(writer_sink, 10)
    view_data = transform_view_data(buffer)
    film_views_from_kafka = consume_film_views_from_kafka(consumer, view_data)
