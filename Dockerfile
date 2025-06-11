# Set default values for build arguments
ARG PARENT_VERSION=latest-3.12
ARG PORT=8085
ARG PORT_DEBUG=8086

FROM defradigital/python-development:${PARENT_VERSION} AS development

ENV LOG_CONFIG="logging-dev.json"

COPY --chown=nonroot:nonroot pyproject.toml .
COPY --chown=nonroot:nonroot uv.lock .

RUN uv venv \
    && uv sync --frozen --no-cache

COPY --chown=nonroot:nonroot app/ ./app/
COPY --chown=nonroot:nonroot logging-dev.json .

ARG PORT=8085
ARG PORT_DEBUG=8086
ENV PORT=${PORT}
EXPOSE ${PORT} ${PORT_DEBUG}

ENTRYPOINT [ "uv", "run", "--no-sync", "-m", "app.main" ]

FROM defradigital/python:${PARENT_VERSION} AS production

WORKDIR /home/nonroot

ENV LOG_CONFIG="logging.json"

COPY --chown=nonroot:nonroot --from=development /home/nonroot/.venv .venv
COPY --chown=nonroot:nonroot --from=development /home/nonroot/pyproject.toml .
COPY --chown=nonroot:nonroot --from=development /home/nonroot/uv.lock .

COPY --chown=nonroot:nonroot --from=development /home/nonroot/app/ ./app/
COPY --chown=nonroot:nonroot logging.json .

ARG PORT
ENV PORT=${PORT}
EXPOSE ${PORT}

ENTRYPOINT [ "uv", "run", "--no-sync", "-m", "app.main" ]
