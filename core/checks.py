import disnake
from disnake.ext import commands
from tools.exeption import CustomError
from core.models.servers import Servers


class BaseChecks:

    def is_higher(locale_path: object):
        """
        Проверка на топ роль участника

        :return: True или False
        """

        async def predicate(inter: disnake.ApplicationCommandInteraction):
            try:
                locale = locale_path(inter.locale, "errors")
                if inter.guild.owner == inter.author:
                    return True
                member_cheсk = inter.author.top_role <= inter.filled_options[
                    "member" or "участник"
                ].top_role or inter.me.top_role <= inter.filled_options[
                    "member" or "участник"
                ].top_role or inter.filled_options[
                    "member" or "участник"
                ] == inter.guild.owner
                if member_cheсk:
                    raise CustomError(locale["top_role_error"])
                return True
            except KeyError:
                return True

        return commands.check(predicate)

    def self_check(locale_path: object):
        """
        Проверка на использование себя как аргумента

        :return: True или False
        """

        async def predicate(inter: disnake.ApplicationCommandInteraction):
            locale = locale_path(inter.locale, "errors")
            try:
                member = inter.filled_options["member" or "участник"]
            except:
                return True

            if inter.author == member:
                raise CustomError(locale['self_error'])

            return True

        return commands.check(predicate)

    def bot_check(locale_path: object):
        """
        Проверка на использование бота как аргумента

        :return: True или False
        """

        async def predicate(inter: disnake.ApplicationCommandInteraction):
            try:
                locale = locale_path(inter.locale, "errors")
                if inter.filled_options["member" or "участник"].bot:
                    raise CustomError(locale['bot_error'])
                return True
            except KeyError:
                return True

        return commands.check(predicate)

    def vip_check(locale_path: object):
        """
        Проверка на наличие премиума у сервера
        :return: True or False
        """
        async def predicate(inter: disnake.ApplicationCommandInteraction):
            locale = locale_path(inter.locale, "errors")
            server: tuple[Servers, bool] = await Servers.get_or_create(discord_id=inter.guild.id)
            return server[0].vip

        return commands.check(predicate)
