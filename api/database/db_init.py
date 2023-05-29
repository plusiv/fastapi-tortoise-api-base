from tortoise import Tortoise, run_async
from api.settings import env
from .seeders import sample_seeders
from api.database.models import User, Role, Permission


async def init():
    await Tortoise.init(
        config = env.TORTOISE_ORM
    )

    print("Generating Schemas ...")
    await Tortoise.generate_schemas(safe=True if env.ENV == 'production' else False)
    
    print("Start Seeding ...")
    await sample_seeders.run()

# run_async is a helper function to run simple async Tortoise scripts.
run_async(init())
