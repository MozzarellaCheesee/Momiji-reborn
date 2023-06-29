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
    async def hug(
        self,
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

    @BaseChecks.self_check(err)
    @emotion.sub_command(
        name=__("kiss", key="COMMAND_NAME_KISS"),
        description=__('kiss someone', key="COMMAND_DESCRIPTION_KISS")
    )
    async def kiss(
        self,
        inter: AppCmdInter,
        member: disnake.Member = commands.Param(
            name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
            description=__("select member", key="COMMAND_PARAM_DESCRIPTION_MEMBER"),
            default=None
        )
    ):
        locale = _(inter.locale, "kiss")
        embed = disnake.Embed().set_image(url=await get_gif("anime_kiss"))
        embed.description = f"{inter.author.mention} {locale['description_1']} {member.mention}" \
                            if member else f"{inter.author.mention} {locale['description_2']}"

        await inter.send(embed=embed)

    ########################################

    @BaseChecks.self_check(err)
    @emotion.sub_command(
        name=__("punch", key="COMMAND_NAME_PUNCH"),
        description=__('punch someone', key="COMMAND_DESCRIPTION_PUNCH")
    )
    async def punch(
        self,
        inter: AppCmdInter,
        member: disnake.Member = commands.Param(
            name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
            description=__("select member", key="COMMAND_PARAM_DESCRIPTION_MEMBER"),
            default=None
        )
    ):
        locale = _(inter.locale, "punch")
        embed = disnake.Embed().set_image(url=await get_gif("anime_punch"))
        embed.description = f"{inter.author.mention} {locale['description_1']} {member.mention}" \
                            if member else f"{inter.author.mention} {locale['description_2']}"

        await inter.send(embed=embed)

    ########################################

    @BaseChecks.self_check(err)
    @emotion.sub_command(
        name=__("pat", key="COMMAND_NAME_PAT"),
        description=__('pat someone', key="COMMAND_DESCRIPTION_PAT")
    )
    async def pat(
        self,
        inter: AppCmdInter,
        member: disnake.Member = commands.Param(
            name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
            description=__("select member", key="COMMAND_PARAM_DESCRIPTION_MEMBER"),
            default=None
        )
    ):
        locale = _(inter.locale, "pat")
        embed = disnake.Embed().set_image(url=await get_gif("anime_pat"))
        embed.description = f"{inter.author.mention} {locale['description_1']} {member.mention}" \
                            if member else f"{inter.author.mention} {locale['description_2']}"

        await inter.send(embed=embed)

    ########################################

    @emotion.sub_command(
        name=__("smoke", key="COMMAND_NAME_SMOKE"),
        description=__('smoke a cigarette', key="COMMAND_DESCRIPTION_SMOKE")
    )
    async def smoke(self, inter: AppCmdInter):
        locale = _(inter.locale, "smoke")
        await inter.send(
            embed = disnake.Embed(
                description=f"{inter.author.mention} {locale['description_1']}"
            ).set_image(url=await get_gif("anime_smoke"))
        )

    ########################################

    @emotion.sub_command(
        name=__("sad", key="COMMAND_NAME_SAD"),
        description=__('mourn', key="COMMAND_DESCRIPTION_SAD")
    )
    async def sad(self, inter: AppCmdInter):
        locale = _(inter.locale, "sad")
        await inter.send(
            embed = disnake.Embed(
                description=f"{inter.author.mention} {locale['description_1']}"
            ).set_image(url=await get_gif("anime_sad"))
        )

    ########################################


    @BaseChecks.self_check(err)
    @emotion.sub_command(
        name=__("angry", key="COMMAND_NAME_ANGRY"),
        description=__('get angry at someone', key="COMMAND_DESCRIPTION_ANGRY")
    )
    async def angry(
        self,
        inter: AppCmdInter,
        member: disnake.Member = commands.Param(
            name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
            description=__("select member", key="COMMAND_PARAM_DESCRIPTION_MEMBER"),
            default=None
        )
    ):
        locale = _(inter.locale, "angry")
        embed = disnake.Embed().set_image(url=await get_gif("anime_angry"))
        embed.description = f"{inter.author.mention} {locale['description_1']} {member.mention}" \
                            if member else f"{inter.author.mention} {locale['description_2']}"

        await inter.send(embed=embed)

    ########################################

    @BaseChecks.self_check(err)
    @emotion.sub_command(
        name=__("bite", key="COMMAND_NAME_BITE"),
        description=__('bite someone', key="COMMAND_DESCRIPTION_BITE")
    )
    async def bite(
        self,
        inter: AppCmdInter,
        member: disnake.Member = commands.Param(
            name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
            description=__("select member", key="COMMAND_PARAM_DESCRIPTION_MEMBER"),
            default=None
        )
    ):
        locale = _(inter.locale, "bite")
        embed = disnake.Embed().set_image(url=await get_gif("anime_bite"))
        embed.description = f"{inter.author.mention} {locale['description_1']} {member.mention}" \
                            if member else f"{inter.author.mention} {locale['description_2']}"

        await inter.send(embed=embed)

    ########################################

    @BaseChecks.self_check(err)
    @emotion.sub_command(
        name=__("clap", key="COMMAND_NAME_CLAP"),
        description=__('clap someone', key="COMMAND_DESCRIPTION_CLAP")
    )
    async def clap(
        self,
        inter: AppCmdInter,
        member: disnake.Member = commands.Param(
            name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
            description=__("select member", key="COMMAND_PARAM_DESCRIPTION_MEMBER"),
            default=None
        )
    ):
        locale = _(inter.locale, "clap")
        embed = disnake.Embed().set_image(url=await get_gif("anime_clap"))
        embed.description = f"{inter.author.mention} {locale['description_1']} {member.mention}" \
                            if member else f"{inter.author.mention} {locale['description_2']}"

        await inter.send(embed=embed)

    ########################################

    @BaseChecks.self_check(err)
    @emotion.sub_command(
        name=__("feed", key="COMMAND_NAME_FEED"),
        description=__('feed someone', key="COMMAND_DESCRIPTION_FEED")
    )
    async def feed(
        self,
        inter: AppCmdInter,
        member: disnake.Member = commands.Param(
            name=__("member", key="COMMAND_PARAM_NAME_MEMBER"),
            description=__("select member", key="COMMAND_PARAM_DESCRIPTION_MEMBER"),
            default=None
        )
    ):
        locale = _(inter.locale, "feed")
        embed = disnake.Embed().set_image(url=await get_gif("anime_feed"))
        embed.description = f"{inter.author.mention} {locale['description_1']} {member.mention}" \
                            if member else f"{inter.author.mention} {locale['description_2']}"

        await inter.send(embed=embed)

    ########################################

    @emotion.sub_command(
        name=__("dance", key="COMMAND_NAME_DANCE"),
        description=__('tear up the dance floor', key="COMMAND_DESCRIPTION_DANCE")
    )
    async def dance(self, inter: AppCmdInter):
        locale = _(inter.locale, "dance")
        await inter.send(
            embed = disnake.Embed(
                description=f"{inter.author.mention} {locale['description_1']}"
            ).set_image(url=await get_gif("anime_dance"))
        )

def setup(client: commands.InteractionBot):
    client.add_cog(Emoties(client))