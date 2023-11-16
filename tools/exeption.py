from disnake.ext import commands


class CustomError(commands.CommandError):

    def __init__(self, msg):
        self.msg = msg
        super().__init__(self.msg)
