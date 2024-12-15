FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
CMD ["sh", "-c", "python3 manage.py makemigrations movies && python3 manage.py makemigrations users && python3 manage.py migrate && python3 manage.py import_movies && python3 manage.py runserver 0.0.0.0:8000"]
EXPOSE 8000
