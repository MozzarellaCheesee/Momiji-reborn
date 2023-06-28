import disnake
from disnake.ext import commands
import aiohttp

from core.cog import BaseCog
from os import getenv

async def get_gif(q: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(
                "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit%s&random=%s" % (
                        q,
                        getenv['TENOR_API_KEY'],
                        getenv['TENOR_CLIENT_KEY'],
                        1,
                        True
                )
        ) as response:
            if response.status == 200:
                result = await response.json()
                return result['results'][0]['media_formats']['gif']['url']
            else:
                return None

class Emoties(BaseCog):

    ########################################

    @commands.slash_command(

    )
    async def emotion(self, inter):
        ...

    ########################################

    @emotion.sub_command(

    )
    async def hello(
        self, 
        inter, 
        member: disnake.Member = commands.Param(
            
        )
    ):

        ...

    ########################################

    @emotion.sub_command(description='Обнять кого-то')
    async def hug(self, inter, member: disnake.Member):

        ...

    ########################################

    @emotion.sub_command(description='Поцеловать кого-то')
    async def kiss(self, inter, member: disnake.Member):

        ...

    ########################################

    @emotion.sub_command(description='Ударить кого-то')
    async def punch(self, inter, member: disnake.Member):

        ...

    ########################################

    @emotion.sub_command(description='Погладить кого-то')
    async def pat(self, inter, member: disnake.Member):

        ...

    ########################################

    @emotion.sub_command(description='Курить')
    async def smoke(self, inter):

        ...

    ########################################

    @emotion.sub_command(description='Грустить')
    async def sad(self, inter):

        ...

    ########################################

    @emotion.sub_command(description='Злиться на кого-то')
    async def angry(self, inter, member: disnake.Member = None):

        ...

    ########################################

    @emotion.sub_command(description='Укусить кого-то')
    async def bite(self, inter, member: disnake.Member):

        ...

    ########################################

    @emotion.sub_command(description='Похлопать кому-то')
    async def clap(self, inter, member: disnake.Member = None):

        ...

    ########################################

    @emotion.sub_command(description='Покормить кого-то')
    async def feed(self, inter, member: disnake.Member = None):

        ...

    ########################################

    @emotion.sub_command(description='Танцевать')
    async def dance(self, inter):

        ...