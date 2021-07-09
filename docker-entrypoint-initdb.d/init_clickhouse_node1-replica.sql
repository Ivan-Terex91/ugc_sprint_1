CREATE DATABASE replica;
CREATE TABLE replica.views (user_id String, movie_id String, viewing_progress Int64, viewing_date DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/views', 'replica_2') PARTITION BY toYYYYMMDD(viewing_date) ORDER BY user_id;
CREATE TABLE default.views (user_id String, movie_id String, viewing_progress Int64, viewing_date DateTime) ENGINE = Distributed('company_cluster', '', views, rand());
