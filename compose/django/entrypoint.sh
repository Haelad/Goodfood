#!/bin/sh
set -e  # прекращаем выполнение при ошибке

echo "=== Starting entrypoint ==="

# -----------------------------
# Переменные
# -----------------------------
LOG_DIR="/app/config/logs"
STATIC_DIR="/app/static_collect"
ENV_FILE="/app/.env"

ADMIN_USER="${DJANGO_ADMIN_USER:-admin}"
ADMIN_EMAIL="${DJANGO_ADMIN_EMAIL:-admin@example.com}"
ADMIN_PASSWORD="${DJANGO_ADMIN_PASSWORD:-admin}"


# -----------------------------
# Очистка логов
# -----------------------------
if [ -d "$LOG_DIR" ]; then
  echo "Clearing logs..."
  rm -f "$LOG_DIR"/*.txt
fi

# -----------------------------
# Очистка временных файлов
# -----------------------------
echo "Cleaning temporary files..."
find . -type d -name "__pycache__" -exec rm -rf {} +
rm -rf .pytest_cache

# -----------------------------
# Poetry update/install
# -----------------------------
echo "Installing/updating dependencies..."
poetry install --no-interaction --no-ansi
poetry update --no-interaction --no-ansi

# -----------------------------
# Миграции
# -----------------------------
echo "Applying migrations..."
poetry run python manage.py migrate --noinput

# -----------------------------
# Создание суперпользователя
# -----------------------------
echo "Ensuring superuser exists..."
poetry run python manage.py shell << END
import os
from django.contrib.auth import get_user_model
User = get_user_model()

ADMIN_USER = os.environ.get('DJANGO_ADMIN_USER', 'admin')
ADMIN_EMAIL = os.environ.get('DJANGO_ADMIN_EMAIL', 'admin@example.com')
ADMIN_PASSWORD = os.environ.get('DJANGO_ADMIN_PASSWORD', 'admin')

if not User.objects.filter(username=ADMIN_USER).exists():
    User.objects.create_superuser(ADMIN_USER, ADMIN_EMAIL, ADMIN_PASSWORD)
END
# -----------------------------
# Сбор статики (prod)
# -----------------------------
if [ "$DJANGO_ENV" = "production" ]; then
    echo "Collecting static files..."
    poetry run python manage.py collectstatic --noinput
fi

# -----------------------------
# Запуск сервера
# -----------------------------
echo "Starting server..."
exec poetry run "$@"
