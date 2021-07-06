import os

PROJECT_NAME = os.getenv("PROJECT_NAME", "loader_data_to_kafka")

KAFKA_DSN = os.getenv("BOOTSTRAP_SERVER", "localhost:9092")

AUTH_URL = os.getenv("AUTH_URL", "http://localhost:8001/")

TOPIC = os.getenv("MOVIE_VIEWS_TOPIC", "views")
