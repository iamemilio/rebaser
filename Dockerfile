FROM python:2-slim-stretch

RUN groupadd -r rebaser && useradd --no-log-init -r -g rebaser -u 1037810000 rebaser
RUN apt update && apt install -y git && pip install gitpython pygithub
