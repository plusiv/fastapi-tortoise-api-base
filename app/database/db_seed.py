from tortoise import Tortoise, run_async
from app.core.settings import TORTOISE_ORM
from .seeders import sample_seeders


async def init():
    await Tortoise.init(config=TORTOISE_ORM)

    print("Start Seeding ...")
    await sample_seeders.run()


# run_async is a helper function to run simple async Tortoise scripts.
run_async(init())
