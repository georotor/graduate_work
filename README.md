# Movies: Ассистент
[![CI](https://github.com/georotor/movies_assistant/actions/workflows/tests.yml/badge.svg)](https://github.com/georotor/movies_assistant/actions/workflows/tests.yml)

Сервис интеграции между сервисом поиска фильмов и голосовыми помощниками `Алиса` и `Маруся`.

Реализованные возможности:
- Обработка входящих запросов
- Выделением намерений и сущностей из сообщения
- Поиск информации по запрашиваемому кинопроизведению  

## Архитектура
![Архитектура](https://github.com/georotor/movies_assistant/blob/main/docs/schema.png?raw=true)


## Компоненты сервиса
- [API обработки входящих запросов](https://github.com/georotor/movies_assistant/tree/main/assistant)
- [Сервис выделения намерений и сущностей](https://github.com/georotor/movies_assistant/tree/main/nlu_rasa)
- [API поиска информации по кинопроизведению](https://github.com/georotor/movies_async_api)
- [ETL заполнения поисковой БД](https://github.com/georotor/movies_etl)

## Запуск сервиса

`git clone --recurse-submodules git@github.com:georotor/movies_assistant.git`

Для запуска потребуется 3 файла с переменными окружения:

- `.env.assist` с настройками для API: 
  - `cp .env.assist.example .env.assist`
- `.env.db` с настройками для Postgres: 
  - `cp .env.db.example .env.db`
- `.env.etl` с настройками для ETL: 
  - `cp .env.etl.example .env.etl`

Запуск осуществляется командой: `docker-compose up --build`

После старта будет доступен [Swagger API](http://127.0.0.1/api/openapi).

## Тестирование
```
docker-compose -f assistant/src/tests/functional/docker-compose.yml up --build tests
```
