from core.settings import DB_URL
from tortoise import Tortoise
import logging


async def init_database():
    await Tortoise.init(
        db_url=DB_URL, 
        modules={
            "models": [
                "core.models.users",
                "core.models.families",
                "core.models.profiles",
                "core.models.channels",
                "core.models.tickets",
                "core.models.warns",
                "core.models.servers",
                "core.models.authorized_sessions",
                "core.models.roles"
            ]
        }
    )
    # await Tortoise.generate_schemas(safe=True)
    logging.info("База данных подключена")
