import os

from coroutines import (consume_film_views_from_kafka, transform_view_data,
                        write_to_clickhouse)
from kafka import KafkaConsumer

from clickhouse_driver import Client

if __name__ == "__main__":
    consumer = KafkaConsumer(
        os.getenv("MOVIE_VIEWS_TOPIC"),
        bootstrap_servers=[os.getenv("BOOTSTRAP_SERVER")],
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        group_id="kafka-to-clickhouse",
        api_version=(0, 10, 1),
    )
    db = Client(host='clickhouse-node1')

    writer_sink = write_to_clickhouse(consumer, os.getenv("MOVIE_VIEWS_TOPIC"), db)
    view_data = transform_view_data(writer_sink)
    film_views_from_kafka = consume_film_views_from_kafka(consumer, view_data)
