# Set default values for build arguments
ARG BASE_VERSION=3.12.10-slim
ARG PORT=8085
ARG PORT_DEBUG=8086

FROM python:${BASE_VERSION} AS development

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHON_ENV=development

RUN addgroup --gid 1000 python \
  && adduser python \
    --uid 1000 \
    --gid 1000 \
    --home /home/python \
    --shell /bin/bash

ENV PATH="/home/python/.local/bin:$PATH"

USER python

RUN python -m pip install --user uv

WORKDIR /home/python/app

COPY --chown=python:python pyproject.toml .
COPY --chown=python:python uv.lock .

RUN uv sync --frozen

COPY --chown=python:python app/ ./app/
COPY --chown=python:python logging-dev.json .

ARG PORT=8085
ARG PORT_DEBUG=8086
ENV PORT=${PORT}
EXPOSE ${PORT} ${PORT_DEBUG}

CMD ["uv", "run", "--no-sync", "-m", "app.main"]

FROM python:${BASE_VERSION} AS production

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHON_ENV=production

ENV PATH="/home/python/.local/bin:$PATH"

# CDP PLATFORM HEALTHCHECK REQUIREMENT
RUN apt update  \
  && apt install curl -y

RUN addgroup --gid 1000 python \
  && adduser python \
    --uid 1000 \
    --gid 1000 \
    --home /home/python \
    --shell /bin/bash

USER python

RUN python -m pip install --user uv

WORKDIR /home/python/app

COPY --chown=python:python --from=development /home/python/app/pyproject.toml .
COPY --chown=python:python --from=development /home/python/app/uv.lock .

RUN uv sync --frozen --no-dev

COPY --chown=python:python --from=development /home/python/app/app ./app/
COPY --chown=python:python logging.json .

ARG PORT
ENV PORT=${PORT}
EXPOSE ${PORT}

CMD ["uv", "run", "--no-sync", "-m", "app.main"]
