import logging

import uvicorn as uvicorn
from aiokafka import AIOKafkaProducer
from core import auth, config, my_kafka
from core.auth import AuthClient, auth_current_user
from core.logger import LOGGING
from core.my_kafka import get_kafka_producer
from fastapi import Depends, FastAPI
from fastapi.responses import ORJSONResponse
from models.progress_film import ProgressFilmModel

app = FastAPI(
    title=config.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    auth.auth_client = AuthClient(base_url=config.AUTH_URL)
    my_kafka.kafka_producer = AIOKafkaProducer(bootstrap_servers=config.KAFKA_DSN)
    await my_kafka.kafka_producer.start()


@app.on_event("shutdown")
async def shutdown():
    await my_kafka.kafka_producer.stop()


@app.post("/progress-film/", tags=["produce_received_data"])
async def kafka_produce_received_data(
    progress_film: ProgressFilmModel,
    auth_user=Depends(auth_current_user),
    producer: AIOKafkaProducer = Depends(get_kafka_producer),
):
    await producer.send(
        topic=config.TOPIC,
        value=progress_film.json().encode(),
        key=f"{progress_film.user_id}_{progress_film.movie_id}".encode(),
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=9999,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
