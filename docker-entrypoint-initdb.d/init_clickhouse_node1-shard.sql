CREATE DATABASE shard;
CREATE TABLE shard.views (user_id String, movie_id String, viewing_progress Int64, viewing_date DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/views', 'replica_1') PARTITION BY toYYYYMMDD(viewing_date) ORDER BY user_id;

