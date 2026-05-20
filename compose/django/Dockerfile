FROM python:3.12-slim
 
WORKDIR /app
 
# Системные зависимости
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        postgresql-client curl gcc libpq-dev libmagic1 && \
    pip install --upgrade pip && \
    pip install poetry && \
    apt-get purge -y gcc libpq-dev && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
 
# Копируем только файлы зависимостей — чтобы Docker кэшировал этот слой
# и не переустанавливал пакеты при каждом изменении кода
COPY pyproject.toml poetry.lock /app/
 
# ARG позволяет передавать параметр при сборке:
#   dev:  docker build --build-arg ENV=dev .
#   prod: docker build .  (или --build-arg ENV=production)
ARG ENV=production
 
RUN if [ "$ENV" = "dev" ]; then \
        poetry install --no-root; \
    else \
        poetry install --only main --no-root; \
    fi
 
# Копируем код приложения
COPY . /app/
 
COPY compose/django/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
 
EXPOSE 8000
 
ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
