## Меняем структуру проекта

После завершения разработки проект должен выглядеть примерно так:

```
jr_project_db/
├── adminapp/
├── conftest.py
├── main/
├── manage.py
├── media/
├── pytest.ini
├── shop/
├── static/
├── templates/
├── tests/
├── user/
│
├── docker-compose.yml
├──  README.md
├──  requirements.txt
├── .gitignore
└── .env
```


Django-часть проекта необходимо будет переместить в директорию `app`:

```html
project/
├── docker-compose.yml
├── Dockerfile
├── nginx/
│   └── nginx.conf
├── app/                <-- Переносим Django проект в app
│   ├── adminapp/
│   ├── conftest.py
│   ├── main/
│   ├── make_file_tree.py
│   ├── manage.py
│   ├── media/
│   ├── pytest.ini
│   ├── requirements.txt
│   ├── shop/
│   ├── static/
│   ├── templates/
│   ├── tests/
│   └── user/
│
├──  README.md
├── .gitignore
└── .env
```

⚠️ ВНИМАНИЕ!!!
Убедитесь, что при переносе проекта "добрый" PyCharm не добавил в пути импорта `app`!

## Добавляем `Dockerfile`:

```yaml
FROM python:3.12-slim

WORKDIR /app

# Устанавливаем системные зависимости (нужны для psycopg2)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app .

CMD ["gunicorn", "main.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## Изменяем текущий `docker-compose.yml` на:

```yaml
services:
  db:
    image: postgres:17
    env_file:
      - .env
    ports:
      - "5435:5432"
    volumes:
      - jr_project_postgres_db_data:/var/lib/postgresql/data
    restart: always

  web:
    build: .
    command: >
      sh -c "python manage.py collectstatic --noinput &&
             gunicorn main.wsgi:application --bind 0.0.0.0:8000"
    env_file:
      - .env
    depends_on:
      - db
    volumes:
      - ./app:/app
      - static_volume:/app/collectstatic
    expose:
      - "8000"
    restart: always

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - static_volume:/app/collectstatic:ro
    depends_on:
      - web
    restart: always

volumes:
  jr_project_postgres_db_data:
  static_volume:
```
⚠️ ВНИМАНИЕ!!!
Как видим, статика АВТОМАТИЧЕСКИ создаётся (обновляется) в папке
`/app/collectstatic`

## Добавляем файл `nginx/nginx.conf`

```
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    upstream django {
        server web:8000;
    }

    server {
        listen 80;

        location /static/ {
            alias /app/collectstatic/;
        }

        location / {
            proxy_pass http://django;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}

```

## В `app/requirements.txt` добавляем `gunicorn`

```
gunicorn
```

## Изменяем `settings.py`:

1. **Добавить:**

```python

# Папка, куда collectstatic будет собирать все файлы
STATIC_ROOT = BASE_DIR / "collectstatic"

```

2. **Заменить настройки почты из `local_settings.py`**   
(чтобы сэкономить на добавлении отдельного тома)

```python
SITE_URL = "http://127.0.0.1:8000"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.getenv("EMAIL_NAME", "email_name")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_PASSWORD", "email_password")
SERVER_EMAIL = os.getenv("EMAIL_NAME", "email_name")
DEFAULT_FROM_EMAIL = os.getenv("EMAIL_NAME", "email_name")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

## Изменить настройки в `.env`

1. **Исправить** 

```yaml
DJANGO_DB_HOST=localhost
DJANGO_DB_PORT=5435
```

на

```yaml
DJANGO_DB_HOST=db
DJANGO_DB_PORT=5432
```

2. **И добавить**

```yaml
# variables for email
EMAIL_NAME=ваша-почта-без-кавычек
EMAIL_PASSWORD=ваш-пароль-без-кавычек
```