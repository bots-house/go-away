FROM python:3.8.6-slim-buster AS dev_build

ENV STAGE='production' \
  BUILD_ONLY_PACKAGES='wget' \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.1.4 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  PATH="$PATH:/root/.poetry/bin"

# System deps:
RUN apt-get update \
  && apt-get install --no-install-recommends -y \
  bash \
  build-essential \
  curl \
  # Installing `poetry` package manager:
  # https://github.com/python-poetry/poetry
  && curl -sSL 'https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py' | python \
  && poetry --version \
  # Cleaning cache:
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR /runtime

COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x '/docker-entrypoint.sh'

COPY ./poetry.lock ./pyproject.toml /runtime/

RUN echo "$STAGE" \
  && poetry install \
  $(if [ "$STAGE" = 'production' ]; then echo '--no-dev'; fi) \
  --no-interaction --no-ansi --no-root

COPY . /runtime

RUN echo "$STAGE" \
  && poetry install \
  --no-dev --no-interaction --no-ansi \
  && if [ "$STAGE" = 'production' ]; then rm -rf "$POETRY_CACHE_DIR"; fi

EXPOSE 4321

CMD ["python", "-m", "go_away"]
ENTRYPOINT ["/docker-entrypoint.sh"]
