from dotenv import dotenv_values

config = dotenv_values()
DB_URL="mysql://root@localhost:3306/momiji"

commands_ = {
    "extensions.commands.accounts",
    "extensions.commands.developer",
    "extensions.commands.economy",
    "extensions.commands.family",
    "extensions.commands.gaiety",
    "extensions.commands.info",
    "extensions.commands.moderation",
    "extensions.commands.rating",
    "extensions.commands.roleplay",
    "extensions.commands.server_settings",
    "extensions.commands.user",
    "extensions.commands.utilits",
}
events = {
    "extensions.events.levels",
    "extensions.events.on_error",
    "extensions.events.on_guild_join",
    "extensions.events.on_guild_remove",
    "extensions.events.on_member_join",
    "extensions.events.on_member_remove",
    "extensions.events.on_ready",
}