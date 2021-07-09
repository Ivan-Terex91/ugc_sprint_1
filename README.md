# Проектная работа 8 спринта

Проектные работы в этом модуле выполняются в команда по 3 человека. Процесс обучения аналогичен сервису, где вы изучали асинхронное программирование. Роли в команде и отправка работы на ревью не меняются.

Распределение по командам подготовит команда сопровождения. Куратор поделится с вами списками в Slack в канале `#breaking_news`.

Командный модуль так же означает возвращение демо с наставником.

Задания на спринт вы найдёте внутри тем.


# Запуск проекта

1. Скопировать переменные окружения командой `make copy_env_file`.
2. Запустить `docker-compose up -d --build`


[Отрисовка архитектуры](https://github.com/Ivan-Terex91/ugc_sprint_1/pull/8)
1. Добавлены скрипт и UML диаграмма AS IS
2. Добавлены скрипт и UML диаграмма TO BE, диграмма немного подкорректированна в [коммите](https://github.com/Ivan-Terex91/ugc_sprint_1/commit/fcc5997bbdd5fd711da23fdf7447532cb2c55e87)


[Docker-compose](https://github.com/Ivan-Terex91/ugc_sprint_1/pull/9)
1. Добавлен файл docker-compose
2. Добавлены конфиги для ClickHouse


[Сервис по загрузке данных в Kafka](https://github.com/Ivan-Terex91/ugc_sprint_1/pull/13)
1. Cервис, который принимает и отправляет данные в Kafka
2. Добавлен сервис auth из предыдущего спринта
3. Проверка актуальности токена
4. Dockerfile для сервиса


[Загрузка данных из Kafka](https://github.com/Ivan-Terex91/ugc_sprint_1/pull/12/)
1. Добавлена загрузка данных из Kafka


[Загрузка данных в ClickHouse](https://github.com/Ivan-Terex91/ugc_sprint_1/pull/14/)
1. Добавлена загрузка данных в ClickHouse
2. Создание необходимых таблиц при запуске
