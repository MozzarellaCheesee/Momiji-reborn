import disnake
from tortoise.queryset import Prefetch

def divide_chunks(lst, n):

    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_avatar_formats(member: disnake.User | disnake.Member) -> list[str]:

    """
    Вовращает список с ссылками на различные размеры аватара пользователя (поддерживает анимированные аватарки)
    :param member: пользователь
    :return: список со ссылками на различные размеры аватарки
    """

    formats = [
        f"[PNG]({member.display_avatar.replace(format='png', size=1024).url})",
        f"[JPG]({member.display_avatar.replace(format='jpg', size=1024).url})"
    ]

    if member.display_avatar.is_animated():
        formats.append(f"[GIF]({member.display_avatar.replace(format='gif', size=1024).url})")
    return formats

def split_guild_members(guild_members: list[disnake.Member]) -> tuple[list[disnake.Member], ...]:

    """
    Разделяет пользователей и ботов
    :param guild_members:
    :return:
    """

    bots = []
    users = []

    for m in guild_members:
        if m.bot:
            bots.append(m)
        else:
            users.append(m)

    return bots, users


async def get_member_profile(member, client, to_prefetch: list[str | Prefetch] = None):

    """
    Возвращает профиль участника
    :inter:
    :client:
    :return: profile
    """

    user_in_db = await client.db.Users.get(discord_id=member.id)
    server_in_db = await client.db.Servers.get(discord_id=member.guild.id)
    if to_prefetch is None:
        profile = await client.db.Profiles.get(user=user_in_db, server=server_in_db)
    else:
        profile = await client.db.Profiles.get(user=user_in_db, server=server_in_db).prefetch_related(to_prefetch)
    return profile

async def standard_emb(
        member: disnake.Member = None,
        description: str = None,
        title: str = None) -> disnake.Embed:
    emd = disnake.Embed(
        color=0x2b2d31,
        description=description,
        title=title)
    if member is not None:
        emd.set_thumbnail(url=member.display_avatar)
    return emd