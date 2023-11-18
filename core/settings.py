from dotenv import dotenv_values

config = dotenv_values()
DB_URL="mysql://p527749_astolfo_owo:AstolfoServant13_@185.105.110.5:3306/p527749_momiji_db"

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