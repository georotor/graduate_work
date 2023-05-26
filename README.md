# Ассистент

https://github.com/georotor/graduate_work

Сервис интеграции между сервисом поиска фильмов и голосовыми помощниками `Алиса` и `Маруся`.

Реализованные возможности:
- Обработка входящих запросов
- Выделением намерений и сущностей из сообщения
- Поиск информации по запрашиваемому кинопроизведению  

## Архитектура
![Архитектура](https://github.com/georotor/graduate_work/blob/main/docs/schema.png?raw=true)


## Компоненты сервиса
- [API обработки входящих запросов](https://github.com/georotor/graduate_work/tree/main/assistant)
- [Сервис выделения намерений и сущностей](https://github.com/georotor/graduate_work/tree/main/nlu_rasa)
- [API поиска информации по кинопроизведению](https://github.com/georotor/async_api)
- [ETL заполнения поисковой БД](https://github.com/georotor/etl_movies)

## Запуск сервиса

`git clone --recurse-submodules git@github.com:georotor/graduate_work.git`

Для запуска потребуется 3 файла с переменными окружения:

- `.env.assist` с настройками для API: 
  - `cp .env.assist.example .env.assist`
- `.env.db` с настройками для Postgres: 
  - `cp .env.db.example .env.db`
- `.env.etl` с настройками для ETL: 
  - `cp .env.etl.example .env.etl`

Запуск осуществляется командой: `docker-compose up --build`

После старта будет доступен [Swagger API](http://127.0.0.1/api/openapi).





