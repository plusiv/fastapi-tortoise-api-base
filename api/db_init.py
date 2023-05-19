import random
from faker import Faker
from tortoise import Tortoise, run_async
from .database.models import User, User_Pydantic, Role, Role_Pydantic
from .database.settings import TORTOISE_ORM
from . import env


async def basic_seeders(): 
    f = Faker(['es_ES'])

    # Insert Roles
    roles = {
            "viewer": ["view"], 
            "editor": ["view", "update"], 
            "admin": ["view", "add", "update", "delete"]
            }

    roles_list = []
    async for role_name in roles:
        role_pydantic = Role_Pydantic(title=role_name.capitalize(), slug=role_name)
        role = await Role.create(**role_pydantic.dict(exclude_unset=True))
        
        # Insert Permission
        permissions_list = []
        async for permission_name in roles.get(role_name):
           permission_pydantic = Permission_Pydantic(title=permission_name.capitalize(), slug=permission_name)
           permission = Permission(**permission_pydantic.dict(exclude_unset=True))
           permission = await Permission.get_or_create(permission)
           permissions_list.append(permission)

        role.permission.add(*permissions_list)
        roles_list.append(role)

    # Insert Users
    NUMBER_OF_USERS = 10
    for _ in range(NUMBER_OF_USERS):
        user = {
                "username": f.simple_profile().get('username'),
                "first_name": f.first_name(),
                "last_name": f.last_name(),
                "hashed_password": "",
                "email": f.ascii_email(), 
                "sex": f.boolean(),
                "birthday": date_of_birth(),
                }
        user_pydantic = User_Pydantic(**user)
        user = User.create(**user_pydantic, role = random.choise(roles_list))


async def init():
    await Tortoise.init(
        config = TORTOISE_ORM
    )
    # Generate the schema
    await Tortoise.generate_schemas(safe=True if env.get('ENV', default='dev') == 'production' else False)
    await basic_seeders()

# run_async is a helper function to run simple async Tortoise scripts.
run_async(init())
