FROM python:3.11-bullseye
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends gcc musl-dev default-libmysqlclient-dev
RUN pip install --upgrade pip

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . /app
WORKDIR /app
ENV PYTHONPATH /app