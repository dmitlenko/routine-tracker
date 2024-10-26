FROM python:3.12.0-slim

ENV PYTHONBUFFERED=1 \
    POETRY_VERSION=1.8.3 \
    POETRY_VIRTUALENVS_CREATE="false"

RUN apt-get update && apt-get install -y gettext

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY poetry.lock pyproject.toml docker/django/docker-entrypoint.sh /app/

RUN poetry install --no-interaction --no-ansi --without dev

COPY routine_tracker/ /app/routine_tracker/

RUN chmod +x docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]
