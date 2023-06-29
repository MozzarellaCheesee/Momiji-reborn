import disnake
from disnake import Localized as __
from disnake import AppCmdInter
from disnake.ext import commands

from core.cog import BaseCog
from core.i18n import LocalizationStorage
from core.checks import BaseChecks
from core.settings import config

import aiohttp

_ = LocalizationStorage("roleplay")
err = LocalizationStorage("errors#2")

async def get_gif(q: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit%s&random=%s" % (
                        q,
                        config['TENOR_API_KEY'],
                        config['TENOR_CLIENT_KEY'],
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
        name=__("roleplay", key="COMMAND_GROUP_ROLEPLAY")
    )
    async def emotion(self, inter: AppCmdInter):
        ...

    ########################################

    @BaseChecks.self_check(err)
    @emotion.sub_command(
        name=__("hello", key="COMMAND_NAME_HELLO"),
        description=__('greet someone', key="COMMAND_DESCRIPTION_HELLO")
    )
    async def hello(
        self, 
        inter: AppCmdInter, 
        member: disnake.Member = commands.Param(
            name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
            description=__("select member", key="COMMAND_PARAM_DESCRIPTION_MEMBER"),
            default=None
        )
    ):
        locale = _(inter.locale, "hello")
        embed = disnake.Embed().set_image(url=await get_gif("anime_hello"))
        embed.description = f"{inter.author.mention} {locale['description_1']} {member.mention}" \
                            if member else f"{locale['description_2']}"

        await inter.send(embed=embed)
            

    ########################################

    @BaseChecks.self_check(err)
    @emotion.sub_command(
        name=__("hug", key="COMMAND_NAME_HUG"),
        description=__('hug someone', key="COMMAND_DESCRIPTION_HUG")
    )
    async def hug(self,
        inter: AppCmdInter,
        member: disnake.Member = commands.Param(
            name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
            description=__("select member", key="COMMAND_PARAM_DESCRIPTION_MEMBER"),
            default=None
        )
    ):
        locale = _(inter.locale, "hug")
        embed = disnake.Embed().set_image(url=await get_gif("anime_hug"))
        embed.description = f"{inter.author.mention} {locale['description_1']} {member.mention}" \
                            if member else f"{inter.author.mention} {locale['description_2']}"

        await inter.send(embed=embed)

    ########################################

    @emotion.sub_command()
    async def kiss(self, inter, member: disnake.Member):

        ...

    ########################################

    @emotion.sub_command()
    async def punch(self, inter, member: disnake.Member):

        ...

    ########################################

    @emotion.sub_command()
    async def pat(self, inter, member: disnake.Member):

        ...

    ########################################

    @emotion.sub_command()
    async def smoke(self, inter):

        ...

    ########################################

    @emotion.sub_command()
    async def sad(self, inter):

        ...

    ########################################

    @emotion.sub_command()
    async def angry(self, inter, member: disnake.Member = None):

        ...

    ########################################

    @emotion.sub_command()
    async def bite(self, inter, member: disnake.Member):

        ...

    ########################################

    @emotion.sub_command()
    async def clap(self, inter, member: disnake.Member = None):

        ...

    ########################################

    @emotion.sub_command()
    async def feed(self, inter, member: disnake.Member = None):

        ...

    ########################################

    @emotion.sub_command()
    async def dance(self, inter):

        ...

def setup(client: commands.InteractionBot):
    client.add_cog(Emoties(client))