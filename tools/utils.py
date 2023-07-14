import disnake
from tortoise.queryset import Prefetch
from PIL import Image, ImageDraw, ImageFont, Image, ImageChops
from io import BytesIO

def bias(original_x, meaning):
    if len(str(meaning)) == 1:
        return original_x
    new_x: int = original_x - (3 * len(str(meaning)))
    return new_x

def circle(pfp, size=(215, 215)):
    pfp = pfp.resize(size, Image.LANCZOS).convert("RGBA")

    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.LANCZOS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

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

async def _account(locale: dict, client, inter, user):
    user_in_db = await client.db.Users.filter(discord_id=user.id).first().prefetch_related("authorizedsessions")

    if not user_in_db:
        return await inter.send(locale["error"], ephemeral=True)

    await inter.response.defer()

    name = f'{user.name}' if len(user.display_name) <= 10 else f'{user.name}'[:10]+'...'
    card = Image.open('./assets/profile_user.png')
    draw = ImageDraw.Draw(card)

    experience = user_in_db.experience
    messages = user_in_db.messages
    donate_valute = user_in_db.donate_valute
    level = user_in_db.level
    authorizedsessions = len(user_in_db.authorizedsessions)

    avatar_in_png = user.display_avatar.with_static_format("png")
    avatar = circle(Image.open(BytesIO(await avatar_in_png.read())).convert("RGBA"), (142, 141))
    card.paste(avatar, (46, 238), avatar)

    name_font = ImageFont.truetype("assets/fonts/OpenSans_SemiCondensed-ExtraBold.ttf", size=25)
    font = ImageFont.truetype("assets/fonts/OpenSans_SemiCondensed-ExtraBold.ttf", size=15)

    draw.text((215, 280), name, fill="white", font=name_font)
    draw.text((215, 310), f"{locale['not_description']}", fill="grey", font=font)
    draw.text((bias(565, experience), 137), f"{experience}", fill="white", font=font)
    draw.text((bias(565, messages), 328), f"{messages}", fill="white", font=font)
    draw.text((bias(565, donate_valute), 515), f"{donate_valute}", fill="white", font=font)
    draw.text((bias(823, level), 137), f"{level}", fill="white", font=font)
    draw.text((bias(823, authorizedsessions), 328), f"{authorizedsessions}", fill="white", font=font)

    with BytesIO() as image_binary:
        card.save(image_binary, "PNG")
        image_binary.seek(0)

        file = disnake.File(fp=image_binary, filename="image.png")
        await inter.send(file=file)