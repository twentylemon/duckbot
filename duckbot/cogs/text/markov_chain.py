from discord.ext import commands

from duckbot.db import Database


class MarkovChain(commands.Cog):
    def __init__(self, bot, db: Database):
        self.bot = bot
        self.db = db
