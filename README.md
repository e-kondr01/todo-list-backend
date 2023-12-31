# Todo list backend

Using Django Rest Framework

Развёрнутая Swagger документация API:

[http://93.183.72.68:8000/api/schema/swagger-ui/](http://93.183.72.68:8000/api/schema/swagger-ui/)

Для запуска юнит тестов (после установки зависимостей):

```bash
cd app
python manage.py test
```

## Python version
3.11

## Local environment
### Installation
#### Django app
1. Create venv
```bash
python3.11 -m venv .venv
```

2. Activate venv
```bash
source .venv/bin/activate
```

3. Install requirements
```bash
pip install -r app/requirements/local.txt
```

4. Copy .env
```bash
cp app/app/local.example.env app/app/.env
```

#### Docker and Docker compose
Refer to:

https://docs.docker.com/engine/install/

### Usage

Use the script to start PSQL in Docker Compose, apply migrations and run development server:
```bash
make local
```

## Swagger Docs
Go to http://127.0.0.1:8000/api/docs after running server

## Development

During development, use Black formatter, Pylint and Flake8.

## Production environment

### Installation
1. Copy .env:
```bash
cp app/app/production.example.env app/app/.env
```

2. Don't forget to set env variables such as ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS and CORS_ALLOWED_ORIGINS.

### Deploy
Use shortcut script:
```bash
make up
```
