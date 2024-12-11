#!/bin/bash
set -e  # Завершить выполнение, если одна из команд завершится с ошибкой

echo "Применяем миграции..."
python3 manage.py makemigrations movies
python3 manage.py makemigrations users

python3 manage.py migrate

echo "Импортируем фильмы..."
python3 manage.py import_movies

exec "$@"
