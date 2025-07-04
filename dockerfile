FROM python:3.11-slim
# настройка виртуального окружения
# Установка необходимых пакетов и удаление лишнего
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        postgresql-client \
    && apt-get purge -y \
        gcc \
        libpq-dev \
        sqlite3 \
        libsqlite3* \
        binutils \
        perl \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
FROM python:3.11-slim
# настройка виртуального окружения
# Установка необходимых пакетов и удаление лишнего
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        postgresql-client \
    && apt-get purge -y \
        gcc \
        libpq-dev \
        sqlite3 \
        libsqlite3* \
        binutils \
        perl \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Установка зависимостей Python
COPY requirements.txt .
RUN pip install --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt

# Копируем проект

# Установка зависимостей Python
COPY requirements.txt .
RUN pip install --upgrade pip setuptools && \
    pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

EXPOSE 10000

# Запуск сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:10000"]