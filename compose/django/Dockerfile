FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        postgresql-client curl gcc libpq-dev && \
    pip install --upgrade pip && \
    pip install "poetry" && \
    #############################
# REMOVE WHEN U WANT USE PROJECT IN PRODUCTION
    poetry install --with dev && \
    #############################
    poetry install --no-root && \
    apt-get purge -y gcc libpq-dev && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . /app/

COPY compose/django/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

CMD ["poetry", "run", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]