#!/bin/sh

echo "Применяем миграции..."
poetry run python manage.py migrate

echo "Собираем статику..."
poetry run python manage.py collectstatic --noinput

echo "Запускаем сервер..."
exec "$@"