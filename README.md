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
    poetry install
    ```
3. Create `.env` file and add environmental variables values
    ```bash
    cp .env.example .env
    vim .env
    ```
4. Run migrations and seeders (optional):
    ```bash
    poetry shell
    python -m app.database.db_init
    exit
    ```
5. Run project
    ```bash
    poetry shell
    uvicorn --reload app.main:app
    ```
    

