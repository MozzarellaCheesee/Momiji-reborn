from dotenv import dotenv_values

config = dotenv_values()

commands_ = {
    "extensions.commands.info",
    "extensions.commands.moderation",
    "extensions.commands.roleplay",
    "extensions.commands.user"
}

events = {
    "extensions.events.bot_activity",
    "extensions.events.on_error"
}