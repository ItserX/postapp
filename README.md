# postapp

## Обзор проекта

Простой блог‑сервер, написанный на Python с использованием FastAPI, который позволяет хранить публикации в PostgreSQL.
Приложение доступно по публичному адресу http://92.53.104.204:8080 

## Структура проекта

```bash

├── app/                  # исходники приложения
│   ├── config.py         # конфигурация приложения
│   ├── database.py       # подключение к БД
│   ├── main.py           # основной файл приложения FastAPI
│   ├── models.py         # модели SQLAlchemy
│   ├── schemas.py        # Pydantic схемы
├── logs/                 # точка монтирования для логов
├── Dockerfile            # сборка образа приложения
├── docker-compose.yml    # настройка контейнеров
├── init.sql              # схема базы данных
├── README.md             # документация
└── requirements.txt      # зависимости Python
```

## Технологии

- Python 3.12

- FastAPI — веб‑фреймворк для API

- SQLAlchemy — ORM для работы с PostgreSQL

- Pydantic — валидация данных и схемы API

- PostgreSQL — реляционная база данных

- Docker / Docker Compose — контейнеризация

- GitHub Actions — CI/CD для автоматического деплоя

## Запуск локально
1. Настроить переменные окружения(пример)
```bash
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=blog
DB_HOST=db
DB_PORT=5432
DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}

APP_HOST=0.0.0.0
APP_PORT=8080

IMAGE_TAG=latest
DOCKER_USERNAME=itserx
```

2. Запустить через Docker Compose
```bash
docker-compose up --build
```

3. Приложение будет доступно по адресу: http://localhost:8080

## API
1. Получить список публикаций
 
GET /posts
Ответ:
```
[
  { "id": 1, "title": "Hello world", "content": "My first post!" }
]
```
2. Добавить новую публикацию

POST /posts
Тело запроса:
```
{
  "title": "Another post",
  "content": "Some content here"
}
```
Ответ:
```
{
  "id": 2,
  "title": "Another post",
  "content": "Some content here"
}
```

## Проверка работоспособности

1. Убедиться, что контейнеры запущены и доступны по порту 8080. 

2. Сделать GET-запрос к /posts — ожидаем пустой массив или существующие публикации.

3. Сделать POST-запрос к /posts с новой публикацией.

4. Снова GET /posts — публикация должна появиться в списке.

## Деплой через GitHub Actions
При пуше в ветку main workflow выполняет:

1. Сборку Docker-образа приложения.

2. Публикацию образа на Docker Hub.

3. Деплой на сервер по SSH с обновлением контейнеров через Docker Compose.

### Необходимые секреты GitHub Actions:
```
SSH_HOST — IP или домен сервера

SSH_USER — пользователь для SSH

SSH_KEY — приватный ключ для доступа к серверу

DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT — настройки БД

APP_HOST, APP_PORT — адрес и порт приложения

DOCKER_USERNAME, DOCKER_PASSWORD — данные для Docker Hub
```

На сервере workflow автоматически создаёт файл .env с переменными окружения и поднимает контейнеры.
