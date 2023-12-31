# Используйте официальный образ Python в качестве базового образа
FROM python:3.10

# Установите зависимости приложения
RUN apt-get update && apt-get install -y --no-install-recommends gcc
RUN pip install --upgrade pip
RUN pip install fastapi
RUN pip install uvicorn
RUN pip install sqlalchemy
RUN pip install asyncpg
RUN pip install requests
RUN pip install ujson
RUN pip install psycopg2

# Установите рабочую директорию
WORKDIR /quiz

# Копируйте содержимое директории проекта в рабочую директорию контейнера
COPY . /quiz

# Запустите приложение при помощи uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]