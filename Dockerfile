# Используем базовый образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . /app/

# Выполняем команды миграций и импортов перед запуском сервера
CMD ["sh", "-c", "python3 manage.py makemigrations movies && python3 manage.py makemigrations users && python3 manage.py migrate && python3 manage.py import_movies && python3 manage.py runserver 0.0.0.0:8000"]

# Открываем порт для приложения
EXPOSE 8000
