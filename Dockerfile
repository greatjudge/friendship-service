# базовый образ
FROM python:3

# Создаем папку friendship и устнавливаем рабочий каталог контейнера
WORKDIR /friendship

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt ./
# Устанавливаем библиотеки из requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем все файлы из локального проекта в контейнер
COPY . /

# Указывем, какой порт будет прослушивать контейнер
EXPOSE 8000

RUN chmod +x /backend-entrypoint.sh
ENTRYPOINT '../backend-entrypoint.sh'