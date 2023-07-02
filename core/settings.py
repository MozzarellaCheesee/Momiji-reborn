from dotenv import dotenv_values

config = dotenv_values()

commands_ = {
    "extensions.commands.info",
    "extensions.commands.moderation",
    "extensions.commands.roleplay",
    "extensions.commands.user",
    "extensions.commands.utilits"
}

events = {
    "extensions.events.on_ready",
    "extensions.events.on_error"
}