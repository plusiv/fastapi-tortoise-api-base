# -*- coding: utf-8 -*-
from tortoise import Tortoise, run_async
from app.core.settings import TORTOISE_ORM
from app.database.seeders import sample_seeders


async def init():
    await Tortoise.init(config=TORTOISE_ORM)

    print("Start Seeding ...")
    await sample_seeders.generate_seeders()


# run_async is a helper function to run simple async Tortoise scripts.
run_async(init())
