# FastAPI Template Project

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com)
[![GitHub Super-Linter](https://github.com/plusiv/fastapi-tortoise-api-base/actions/workflows/lint.yaml/badge.svg)](https://github.com/marketplace/actions/super-linter)

This is a template project for building API applications using FastAPI, Poetry, and Tortoise ORM. The base project is about a To-Do application, so, feel free of removing every line of code outside of your needs.

## Prerequisites

Make sure you have the following installed before setting up the project:

- Python 3.11.3 or above
- [Poetry](https://python-poetry.org/)
- [Docker](https://www.docker.com/) (optional, required for running the database with Docker)

## Project Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/plusiv/fastapi-tortoise-api-base.git
   cd fastapi-tortoise-api-base
   ````

2. Install the project dependencies using Poetry:

    ```bash
    # This will install all project dependencies.
    poetry install
    ```

    _Optionally install [pre-commit](https://pre-commit.com/) hooks._

    ```bash
    # Install pre-commit (optional)
    poetry run pre-commit install
    ```

3. Create `.env` file and add environmental variables values

    ```bash
    cp .env.example .env
    vim .env
    ```

4. Run schema creation and seeders (optional):

    ```bash
    poetry run python -m app.database.db_seed
    ```

5. Run project

    ```bash
    poetry run uvicorn --reload app.main:app
    ```

### Tests

To run tests you can enter:

```bash
poetry run pytest
```

### Pre-commit

If you want to run pre-commit to make sure that you're doing a good jon, just run:

```shell
poetry run pre-commit run -a
```

## Tech Stack + Features

### Frameworks

- [FastApi](https://fastapi.tiangolo.com/lo/) – A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

### Database + ORM

- [MySQL](https://www.mysql.com/) - An open-source relational database management system.
- [Tortoise ORM](https://tortoise.github.io/) - Tortoise ORM is an easy-to-use `asyncio` ORM (Object Relational Mapper) inspired by Django.

### Storage

- Minio - __TODO__

### Access Control

- [Casbin](https://github.com/casbin/pycasbin) - An authorization library that supports access control models like ACL, RBAC, ABAC for multiple Languajes.

### Code Quality

- [Super Linter (Github Action)](https://github.com/marketplace/actions/super-linter) - A simple combination of various linters, written in bash, to help validate your source code. Linters are:
  - [Ruff](https://beta.ruff.rs/docs/) - An extremely fast Python linter, written in Rust.
  - [Black](https://github.com/psf/black) - A Python code formatter.
  - [Hadolint (Dockerfile)](https://github.com/hadolint/hadolint) - A smarter Dockerfile linter that helps to build best practice Docker images.
  - Github Actions - A linter for Github Actions.
  - Yaml - A Yaml files linter.
  - Markdown - A Markdown linter.
- [Pre Commit](https://pre-commit.com/) - Git hook scripts are useful for identifying simple issues before submission to code review.
  - check-ast - simply checks whether the files parse as valid python.
  - check-toml - checks toml files for parseable syntax.
  - detect-private-key - detects the presence of private keys.
  - end-of-file-fixer - ensures that a file is either empty, or ends with one newline.
  - fix-encoding-pragma - adds `# -*- coding: utf-8 -*-` to the top of python files.
  - name-tests-test - verifies that test files are named correctly.
  - trailing-whitespace - trims trailing whitespace.
  - black - A Python code formatter.
  - ruff - An extremely fast Python linter, written in Rust.
  - hadolint - A smarter Dockerfile linter that helps to build best practice Docker images.

## Project Structure

This diagram assumes that all folder is a Python module and all of them have a hidden `__init__.py` file.
<!-- You can generate this tree diagram by running: tree -I __pycache__ -I __init__.py -I .git -I .env -I .ruff_cache -I migrations -I .pytest_cache -a . -->

```shell
.
├── .env.example
├── .github
│   └── workflows
│       └── lint.yaml
├── .gitignore
├── .pre-commit-config.yaml
├── Dockerfile
├── LICENSE
├── README.md
├── app
│   ├── core
│   │   ├── email.py
│   │   ├── security
│   │   │   ├── access_control
│   │   │   │   ├── access_control.py
│   │   │   │   ├── model.conf
│   │   │   │   └── policies.csv
│   │   │   ├── hashing.py
│   │   │   └── jwt_handler.py
│   │   ├── settings.py
│   │   └── sms.py
│   ├── database
│   │   ├── crud
│   │   │   ├── todos.py
│   │   │   ├── users.py
│   │   │   └── utils
│   │   │       └── utils.py
│   │   ├── db_seed.py
│   │   ├── models.py
│   │   └── seeders
│   │       └── sample_seeders.py
│   ├── main.py
│   ├── pydantic_models
│   │   ├── messages.py
│   │   ├── todos.py
│   │   ├── tokens.py
│   │   └── users.py
│   ├── routers
│   │   └── v1
│   │       ├── api.py
│   │       ├── dependencies.py
│   │       └── endpoints
│   │           ├── emails.py
│   │           ├── login.py
│   │           ├── sms.py
│   │           ├── todos.py
│   │           └── users.py
│   └── utils
│       └── utils.py
├── docker-compose.yaml
├── poetry.lock
├── pyproject.toml
└── tests
    ├── api
    │   └── endpoints
    │       ├── ping_test.py
    │       └── v1
    │           └── user_test.py
    └── conftest.py
```

### Application folder

```shell
app
├── core
├── database
├── main.py
├── pydantic_models
├── routers
└── utils
```

The `app` folder is the root application folder, there you are goin to found all principal modules:

- `core`: All core modules of the application, such as email, security module, access control and so on.
- `database`: Handles everything about database, such as [CRUDS](https://www.sumologic.com/glossary/crud/), [Tortoise Models](https://tortoise.github.io/models.html), and some sample seeders.
- `main.py`: Main app files, it initializes the entire application.
- `pydantic_models`: This folder contains all Pydantic Models for data validation in all API information exchanges.
- `routers`: All API endpoints versioned.
- `utils`: Helper functions.

### CI

```shell
.github
└── workflows
    └── lint.yaml
```

This project is configured to use [Github Actions](https://github.com/features/actions), and all workflows file can be found in `.github/workflows` as spected.
