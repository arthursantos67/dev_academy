
FROM python:3.12

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat-openbsd \
    && apt-get clean

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/

CMD ["sh", "-c", "while ! nc -z db 5432; do sleep 1; done && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]