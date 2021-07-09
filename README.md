# Проектная работа 8 спринта

Проектные работы в этом модуле выполняются в команда по 3 человека. Процесс обучения аналогичен сервису, где вы изучали асинхронное программирование. Роли в команде и отправка работы на ревью не меняются.

Распределение по командам подготовит команда сопровождения. Куратор поделится с вами списками в Slack в канале `#breaking_news`.

Командный модуль так же означает возвращение демо с наставником.

Задания на спринт вы найдёте внутри тем.

# Настройка Clickhouse

```bash
docker exec -it clickhouse-node1 bash 

clickhouse-client 
```

```sql
CREATE DATABASE shard;
CREATE DATABASE replica;
CREATE TABLE shard.views (user_id String, movie_id String, viewing_progress Int64, viewing_date DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/views', 'replica_1') PARTITION BY toYYYYMMDD(viewing_date) ORDER BY user_id;
CREATE TABLE replica.views (user_id String, movie_id String, viewing_progress Int64, viewing_date DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/views', 'replica_2') PARTITION BY toYYYYMMDD(viewing_date) ORDER BY user_id;
CREATE TABLE default.views (user_id String, movie_id String, viewing_progress Int64, viewing_date DateTime) ENGINE = Distributed('company_cluster', '', views, rand());
exit
exit
```

```bash
docker exec -it clickhouse-node1 bash 

clickhouse-client 
```

```sql
CREATE DATABASE shard;
CREATE DATABASE replica;
CREATE TABLE shard.views (user_id String, movie_id String, viewing_progress Int64, viewing_date DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/views', 'replica_1') PARTITION BY toYYYYMMDD(viewing_date) ORDER BY user_id;
CREATE TABLE replica.views (user_id String, movie_id String, viewing_progress Int64, viewing_date DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/views', 'replica_2') PARTITION BY toYYYYMMDD(viewing_date) ORDER BY user_id;
CREATE TABLE default.views (user_id String, movie_id String, viewing_progress Int64, viewing_date DateTime) ENGINE = Distributed('company_cluster', '', views, rand());
exit
exit
```