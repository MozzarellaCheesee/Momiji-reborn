import disnake
from disnake.ext import commands
from tortoise.queryset import Prefetch
from PIL import ImageDraw, ImageFont, Image, ImageChops
from io import BytesIO
from core.models.profiles import Profiles
from core.models.users import Users


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

    user_in_db = await client.db.Users.get_or_create(discord_id=member.id)
    server_in_db = await client.db.Servers.get_or_create(discord_id=member.guild.id)
    if to_prefetch is None:
        profile = await client.db.Profiles.get_or_none(user=user_in_db[0], server=server_in_db[0])
    else:
        profile = await client.db.Profiles.get(user=user_in_db[0], server=server_in_db[0]).prefetch_related(to_prefetch)
    return profile


async def get_member_profile_for_marry(member, client):
    """
    Возвращает профиль участника
    :inter:
    :client:
    :return: profile
    """

    user_in_db = await client.db.Users.get_or_create(discord_id=member.id)
    server_in_db = await client.db.Servers.get_or_create(discord_id=member.guild.id)
    profile = await client.db.Profiles.get_or_none(user=user_in_db[0], server=server_in_db[0]).select_related("user", "family")
    return profile


async def account(locale: dict, client, inter, user):
    user_in_db = await client.db.Users.get_or_create(discord_id=user.id)
    user_in_db: Users = await user_in_db[0].first().prefetch_related("authorizedsessions")

    if not user_in_db:
        return await inter.send(locale["error"], ephemeral=True)

    await inter.response.defer()

    name = f'{user.name}' if len(user.name) <= 10 else f'{user.name}'[:10] + '...'
    card = Image.open('./assets/profile_user.png')
    draw = ImageDraw.Draw(card)

    experience = user_in_db.experience
    messages = user_in_db.messages
    donate_valute = user_in_db.donate_valute
    level = user_in_db.level
    authorizedsessions = len(user_in_db.authorizedsessions)

    avatar_in_png = user.display_avatar.with_static_format("png")
    avatar = circle(Image.open(BytesIO(await avatar_in_png.read())).convert("RGBA"), (142, 142))
    card.paste(avatar, (46, 238), avatar)

    name_font = ImageFont.truetype("assets/fonts/OpenSans_Condensed-SemiBold.ttf", size=25)
    font = ImageFont.truetype("assets/fonts/OpenSans_Condensed-SemiBold.ttf", size=15)

    draw.text((215, 280), name, fill="white", font=name_font)
    draw.text((215, 310), f"{locale['not_description']}", fill="grey", font=font)
    draw.text((572, 137), f"{experience}", fill="white", font=font, anchor='ma')
    draw.text((572, 328), f"{messages}", fill="white", font=font, anchor='ma')
    draw.text((572, 515), f"{donate_valute}", fill="white", font=font, anchor='ma')
    draw.text((830, 137), f"{level}", fill="white", font=font, anchor='ma')
    draw.text((830, 328), f"{authorizedsessions}", fill="white", font=font, anchor='ma')

    with BytesIO() as image_binary:
        card.save(image_binary, "PNG")
        image_binary.seek(0)

        file = disnake.File(fp=image_binary, filename="image.png")
        await inter.send(file=file)


async def profile(locale: dict, client, inter: disnake.AppCmdInter, user):
    user_in_db = await client.db.Users.get_or_create(discord_id=user.id)
    server_in_db = await client.db.Servers.get_or_create(discord_id=inter.guild.id)
    profile: Profiles = await client.db.Profiles.filter(user=user_in_db[0], server=server_in_db[0]) \
        .prefetch_related("partner", "tickets", "warns_profile").first()

    print('a')

    if not profile:
        print('b')
        return await inter.send(locale["error"], ephemeral=True)
    print('a')

    await inter.response.defer()

    print('a')

    if profile.partner is None:
        partner = locale["no_partner"]
        print('a')
    else:
        partner = inter.guild.get_member(profile.partner.discord_id)
        print('a')

    name = f'@{user.name}' if len(user.name) <= 15 else f'@{user.name}'[:15] + '...'
    card = Image.open('./assets/profile_server.png')
    draw = ImageDraw.Draw(card)

    lvl = profile.level
    message = profile.messages
    open_tickets = len(profile.tickets)
    money = profile.money
    warns = len(profile.warns_profile)

    print('a')

    avatar_in_png = user.display_avatar.with_static_format("png")
    avatar = circle(Image.open(BytesIO(await avatar_in_png.read())).convert("RGBA"), (213, 213))
    card.paste(avatar, (89, 121), avatar)

    name_font = ImageFont.truetype("assets/fonts/OpenSans_Condensed-SemiBold.ttf", size=25)
    font = ImageFont.truetype("assets/fonts/OpenSans_Condensed-SemiBold.ttf", size=15)

    draw.text((110, 350), name, fill='white', font=name_font)
    draw.text((730, 76.5), f"{partner}", fill='white', font=font)
    draw.text((775, 132.5), f"{lvl}", fill='white', font=font, anchor='ma')
    draw.text((775, 187.5), f"{message}", fill='white', font=font, anchor='ma')
    draw.text((775, 242.5), f"{open_tickets}", fill='white', font=font, anchor='ma')
    draw.text((775, 297.5), f"{money}", fill='white', font=font, anchor='ma')
    draw.text((775, 352.5), f"{warns}", fill='white', font=font, anchor='ma')

    with BytesIO() as image_binary:
        card.save(image_binary, "PNG")
        image_binary.seek(0)

        file = disnake.File(fp=image_binary, filename="image.png")
        await inter.send(file=file)


async def love_profile(locale: dict, client: commands.InteractionBot, inter: disnake.AppCmdInter,
                       member: disnake.Member, buttons: disnake.ui.View):
    user_in_db = await client.db.Users.get_or_create(discord_id=member.id)
    server_in_db = await client.db.Servers.get_or_create(discord_id=inter.guild.id)
    profile: Profiles = await client.db.Profiles.filter(
        user=user_in_db[0], server=server_in_db[0]
    ).prefetch_related("family",
                       "family__wife",
                       "family__husband").first()

    if profile is None:
        return await inter.send(locale['error_'].format(member=member.mention), ephemeral=True)

    if profile.family is None:
        return await inter.send(locale['error'].format(member=member.mention), ephemeral=True)

    await inter.response.defer()

    husband: disnake.Member = await client.fetch_user(profile.family.husband)
    wife: disnake.Member = await client.fetch_user(profile.family.wife)

    wife_name = f'{wife.name}' if len(wife.name) <= 15 else f'{wife.name}'[:15] + '...'
    husband_name = f'{husband.name}' if len(husband.name) <= 15 else f'{husband.name}'[:15] + '...'

    wife_avatar = circle(
        Image.open(BytesIO(await wife.display_avatar.with_static_format("png").read())).convert("RGBA"), (230, 230))
    husband_avatar = circle(
        Image.open(BytesIO(await husband.display_avatar.with_static_format("png").read())).convert("RGBA"), (230, 230))

    date_of_create = profile.family.date_of_create.strftime("%d.%m.%Y")
    renewal_date = profile.family.renewal_date.strftime("%d.%m.%Y")

    card = Image.open('./assets/profile_love.png')
    draw = ImageDraw.Draw(card)

    card.paste(wife_avatar, (239, 194), wife_avatar)
    card.paste(husband_avatar, (533, 194), husband_avatar)

    name_font = ImageFont.truetype("assets/fonts/OpenSans_Condensed-SemiBold.ttf", size=20)
    font = ImageFont.truetype("assets/fonts/OpenSans_Condensed-SemiBold.ttf", size=15)

    draw.text((355, 453), wife_name, fill='white', font=name_font, anchor='ma')
    draw.text((649, 453), husband_name, fill='white', font=name_font, anchor='ma')
    draw.text((505, 140), f"{profile.family.money}", fill='white', font=name_font, anchor='ma')
    draw.text((390, 60), locale["date_of_create"], fill='white', font=font, anchor='ma')
    draw.text((610, 60), locale["renewal_date"], fill='white', font=font, anchor='ma')
    draw.text((390, 85), f"{date_of_create}", fill='white', font=name_font, anchor='ma')
    draw.text((610, 85), f"{renewal_date}", fill='white', font=name_font, anchor='ma')

    with BytesIO() as image_binary:
        card.save(image_binary, "PNG")
        image_binary.seek(0)

        await inter.send(
            embed=disnake.Embed(
                title=f"<:momiji_divorce:1175038682818941050> - {locale['button_1']}, :bank: - {locale['button_2']}"
            ).set_image(
                file=disnake.File(fp=image_binary, filename="image.png")

            ),
            view=buttons)


async def get_or_create_role(client: commands.InteractionBot, server: any, _type: str, defaults: dict):
    _server = await client.db.Servers.get_or_create(discord_id=server.id)
    defaults["server"] = _server[0]
    role = await client.db.Roles.get_or_create(defaults=defaults, role_type=_type, server_id=_server[0].id)
    return role
