FROM postgres:17-alpine

# Удаляем ненужные пакеты для минимизации уязвимостей
RUN apk --no-cache del binutils gcc

# По желанию можно обновить систему и PostgreSQL
RUN apk update && apk upgrade --no-cache