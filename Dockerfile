FROM python:3.9

RUN mkdir /app
WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry
COPY ./pyproject.toml .
COPY ./poetry.lock .
RUN poetry config virtualenvs.create false
RUN poetry install

COPY ./ .
