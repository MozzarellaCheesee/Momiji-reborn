from core.settings import DB_URL
from tortoise import Tortoise


async def init_database():
    await Tortoise.init(
        db_url=DB_URL, 
        modules={
            "models": [
                "core.models.users",
                "core.models.families",
                "core.models.banks",
                "core.models.profiles",
                "core.models.channels",
                "core.models.tickets",
                "core.models.warns",
                "core.models.servers",
                "core.models.authorized_sessions"
            ]
        }
    )
    # await Tortoise.generate_schemas(safe=True)