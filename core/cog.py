from disnake.ext import commands


class BaseCog(commands.Cog):

    def __init__(self, client: commands.InteractionBot):
        self.client = client
        
    async def cog_load(self) -> None:
        print(f"Cog {self.__cog_name__} is loaded")

    