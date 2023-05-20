from api import env

#DATABASE_URL = f"{env['DATABASE_TYPE']}://{env['DATABASE_USER']}:{env['DATABASE_USER']}@{env['DATABASE_HOST']}/{env['DATABASE_NAME']}"

TORTOISE_ORM = {
    "connections": {
        "default": {
            'engine': f"tortoise.backends.{env.get('DATABASE_TYPE')}",
            'credentials': {
                'host': env.get('DATABASE_HOST', '127.0.0.1'),
                'port': env.get('DATABASE_PORT', '3306'),
                'user': env.get('DATABASE_USER'),
                'password': env.get('DATABASE_PASSWORD'),
                'database': env.get('DATABASE_NAME'),
            }
        },
    },
    "apps": {
        "models": {"models": ["api.database.models"], "default_connection": "default"},
    },
}
