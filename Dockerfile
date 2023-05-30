#################### Base ####################
ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim AS base

ARG POETRY_VERSION = 1.4.2

ENV WORK_DIR=/usr/app \
    PYTHON_PATH="${WORK_DIR}/venv/bin" \
    PATH=${PYTHON_PATH}:${PATH} \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=${POETRY_VERSION} \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    PORT=3000

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


#################### deps ####################
FROM base as deps

# Install Poetry and its dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential \
    && curl -sSL https://install.python-poetry.org | python3 -

WORKDIR ${PYSETUP_PATH}

COPY poetry.lock pyproject.toml ./

# Install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-dev


#################### development ####################
FROM base as development

WORKDIR $PYSETUP_PATH

# copy in our built poetry + venv
COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# quicker install as runtime deps are already installed
RUN poetry install

WORKDIR ${WORK_DIR}

EXPOSE ${PORT}

CMD ["uvicorn", "--reload", "main:app"]


#################### production ####################
FROM base as production

ENV UID=1112
ENV GID=1112
ENV USER_NAME=python
ENV GROUP_NAME=python
ENV FASTAPI_ENV=production

RUN groupadd -g ${GID} ${GROUP_NAME} && \
    useradd -r -u ${UID} -g ${GROUP_NAME} ${USER_NAME}

COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY ./api ${WORKDIR}

WORKDIR ${WORK_DIR}

USER ${USER_NAME}

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
