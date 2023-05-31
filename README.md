# FastAPI Template Project

This is a template project for building API applications using FastAPI, Poetry, and Tortoise ORM.

## Prerequisites

Make sure you have the following installed before setting up the project:

- Python 3.11.3 or above
- [Poetry](https://python-poetry.org/)
- [Docker](https://www.docker.com/) (optional, required for running the database with Docker)

## Project Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/plusiv/fastapi-tortoise.git
   cd fastapi-tortoise
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
