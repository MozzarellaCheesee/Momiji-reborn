from dotenv import dotenv_values

config = dotenv_values()
DB_URL="mysql://root@localhost:3306/momiji"

commands_ = {
    "extensions.commands.info",
    "extensions.commands.moderation",
    "extensions.commands.roleplay",
    "extensions.commands.user",
    "extensions.commands.utilits",
    "extensions.commands.gaiety"
}
events = {
    "extensions.events.on_ready",
    "extensions.events.on_error"
}