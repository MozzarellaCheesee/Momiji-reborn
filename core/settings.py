from dotenv import dotenv_values

config = dotenv_values()
DB_URL="mysql://root:@localhost:3306/momiji_db"

commands_ = {
    "extensions.commands.accounts",
    "extensions.commands.developer",
    "extensions.commands.economy",
    "extensions.commands.family",
    "extensions.commands.gaiety",
    "extensions.commands.info",
    "extensions.commands.moderation",
    "extensions.commands.profile",
    "extensions.commands.rating",
    "extensions.commands.roleplay",
    "extensions.commands.server_settings",
    "extensions.commands.user",
    "extensions.commands.utilits",
    "extensions.commands.admin"
}
events = {
    "extensions.events.levels",
    "extensions.events.on_error",
    "extensions.events.on_guild_join",
    "extensions.events.on_guild_remove",
    "extensions.events.private_voices",
    "extensions.events.on_ready",
}
