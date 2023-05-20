from tortoise import Tortoise, run_async
from .settings import TORTOISE_ORM
from .seeders import sample_seeders
from api.database.models import User, Role, Permission
from api import env


async def init():
    await Tortoise.init(
        config = TORTOISE_ORM
    )

    print("Generating Schemas ...")
    await Tortoise.generate_schemas(safe=True if env.get('ENV','dev') == 'production' else False)
    
    print("Start Seeding ...")
    await sample_seeders.run()

# run_async is a helper function to run simple async Tortoise scripts.
run_async(init())
