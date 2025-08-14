# README — Taskoro

## Кратко

**Taskoro** — Django-проект с модульной архитектурой (несколько приложений: duels, friends, history, main, note, shop, sim, tasks, tournaments, users и т.д.). Этот репозиторий содержит код сервера, шаблоны, статические файлы и вспомогательные скрипты. README составлен на основе структуры репозитория; некоторые детали (точные требования по зависимостям, способ деплоя) нужно подтвердить по `requirements.txt` и `build.sh`. ([GitHub][1])

---

## Содержание README

* Описание проекта
* Возможности (inferred)
* Стек технологий
* Быстрый старт (локально)
* Конфигурация (.env)
* Структура проекта (обзор приложений)
* Запуск тестов и линтеров
* Деплой (рекомендации)
* Вклад и стиль кодирования
* Roadmap / TODO

---

## Возможности (предполагаемые)


* Пользовательская система (регистрация/профили).
* Друзья / социальные связи (`friends`).
* Дуэли/соревнования (`duels`, `tournaments`).
* Задачи / система миссий (`tasks`).
* Магазин внутриигровых/внутрисистемных товаров (`shop`).
* История действий / логирование (`history`).
* Заметки / личные записи (`note`).
* Шаблоны/статические ресурсы для фронтенда (`templates`, `static`, `media`).
* Скрипт сборки (`build.sh`) и пример данных `data_utf8.json`. 

---

## Технологии

* Django (версия — см. `requirements.txt`)
* Python 3.10+ (рекомендация; уточни в `requirements.txt`)
* HTML / CSS для шаблонов (в проекте много HTML и статических файлов). ###В будущем перейдем на React сделав API

---

## Быстрый старт (локально)

> Ниже — универсальные шаги для запуска Django-проекта. Подставь точные команды/версии по своему окружению.

1. Клонируем репозиторий:

```bash
git clone https://github.com/Dasakami/taskoro.git
cd taskoro
```

2. Создаём виртуальное окружение и устанавливаем зависимости:

```bash
python -m venv .venv
# на Linux / macOS
source .venv/bin/activate
# на Windows (PowerShell)
.venv\Scripts\Activate.ps1

pip install --upgrade pip
pip install -r requirements.txt
```

> Если `requirements.txt` не содержит версий, рекомендую зафиксировать их (например: `pip freeze > requirements.txt` после настройки).

3. Создаём файл окружения `.env` (пример ниже), настраиваем базу данных и другие секреты.

4. Применяем миграции и создаём суперпользователя:

```bash
python manage.py migrate
python manage.py createsuperuser
```

5. (Опционально) Загрузить пример данных:

```bash
python manage.py loaddata data_utf8.json
```

(файл `data_utf8.json` есть в репозитории — убедись, что структура соответствует фикстурам). 

6. Собрать статику и запустить сервер:

```bash
python manage.py collectstatic --noinput
python manage.py runserver
```

7. Для production: рассмотреть использование `gunicorn` + `nginx` или Docker (см. `build.sh`).

---

## Пример `.env` (заменить на реальные значения)

```env
SECRET_KEY="changeme_replace_with_real_value"
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/DBNAME
# или отдельные переменные:
DB_NAME=taskoro_db
DB_USER=taskoro_user
DB_PASSWORD=secret
DB_HOST=localhost
DB_PORT=5432

# Email (если используются нотификации)
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=foo@example.com
EMAIL_HOST_PASSWORD=secret
EMAIL_USE_TLS=True
```

(Подумай о библиотеке `django-environ` или `python-dotenv` для загрузки .env.)

---


## Архитектура / структура проекта (обзор папок)

(кратко, inferred — уточни детали)

* `duels/` — логика дуэлей между пользователями.
* `friends/` — обработка дружбы/запросов на дружбу.
* `history/` — логи/история действий.
* `main/` — основное приложение (homepage, общие настройки).
* `note/` — заметки/личные записи.
* `shop/` — внутренняя экономика / покупки.
* `sim/` — симулятор (вероятно, основная бизнес-логика гейм-части).
* `tasks/` — система заданий/миссий.
* `tournaments/` — турнирная система.
* `users/` — кастомная модель пользователя и управление профилями.
* `templates/`, `static/`, `media/` — фронтенд ресурсы.
* `manage.py`, `requirements.txt`, `build.sh`, `data_utf8.json` — утилиты и конфигурация. 

---

## Деплой (коротко)

* Production-ready: `gunicorn` + `nginx`, SSL (Let's Encrypt).
* Использовать `DATABASE_URL` (Postgres), отдельный static/media сервер (S3/Cloud storage) или nginx.
* Настроить переменные окружения через секреты CI/CD или через systemd/unit.
* Подумать о Healthchecks и логировании (Sentry / ELK).

---

## Вклад (CONTRIBUTING)

1. Fork → feature branch → PR.
2. Описывать изменения в PR и указывать связанные issue.
3. Запускать тесты локально и пройти линтер.
4. Кодстайл: black + isort + flake8 (указать версии).

---

## Roadmap / TODO (предложения)

* Добавить README в корень (готово).
* Добавить `.env.example`.
* Добавить CI (tests, lint).
* Добавить Dockerfile и docker-compose.
* Документировать REST API и модели.
* Автоматизировать импорт `data_utf8.json` (management command).

---

## Примеры команд (стандартные)

```bash
# Миграции
python manage.py makemigrations
python manage.py migrate

# Создать суперпользователя
python manage.py createsuperuser

# Сбор статики
python manage.py collectstatic --noinput

# Запустить тесты
python manage.py test
```

---

## Контакты / поддержка
Gmail:  `dendasakami@gmail.com` 
GitHub:  `https://github.com/Dasakami`
Telegram: `@dandasakami`




