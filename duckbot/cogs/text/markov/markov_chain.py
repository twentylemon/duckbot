from typing import Union

from discord import Member, User
from discord.ext import commands

from duckbot.db import Database


class MarkovChain(commands.Cog):
    def __init__(self, bot, db: Database):
        self.bot = bot
        self.db = db

    @commands.command(name="markovinit")
    async def markov_init_command(self, context, user: Union[User, Member]):
        pass
