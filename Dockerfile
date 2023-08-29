#################### Base ####################
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim AS base

ENV UID=1112 \
    GID=1112 \
    USER_NAME=python \
    GROUP_NAME=python \
    WORK_DIR=/usr/app \
    TEMP_DIR_PATH=/tmp \
    PORT=8000

HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost:${PORT}/api/ping || exit 1

RUN groupadd -g ${GID} ${GROUP_NAME} && \
    useradd -l -r -u ${UID} -g ${GROUP_NAME} ${USER_NAME}

RUN apt-get update && apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

#################### Requirements generation ####################
ARG POETRY_VERSION=1.4.2
FROM base AS requirements-stage


WORKDIR ${TEMP_DIR_PATH}

COPY ./pyproject.toml ./poetry.lock* ${TEMP_DIR_PATH}/

RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}" && \
    poetry export -f requirements.txt --output requirements.txt --without-hashes && \
    poetry export -f requirements.txt --output requirements.dev.txt --without-hashes --with dev


#################### development ####################
FROM base AS development

ENV ENV=development

WORKDIR ${WORK_DIR}

COPY --from=requirements-stage ${TEMP_DIR_PATH}/requirements.dev.txt ${WORK_DIR}/requirements.txt

RUN  pip install --no-cache-dir --upgrade -r "${WORK_DIR}/requirements.txt"

EXPOSE ${PORT}


#################### production ####################
FROM base AS production

ENV ENV=production

WORKDIR ${WORK_DIR}

COPY --from=requirements-stage ${TEMP_DIR_PATH}/requirements.txt ${WORK_DIR}/requirements.txt
RUN pip install --no-cache-dir --upgrade -r "${WORK_DIR}/requirements.txt"

COPY ./app ${WORK_DIR}/app

EXPOSE ${PORT}
USER ${USER_NAME}

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app"]
