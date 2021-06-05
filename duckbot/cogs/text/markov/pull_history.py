from discord import Member, ChannelType, TextChannel, Message
from discord.ext import commands
from typing import List, Optional
from duckbot import DuckBot
from duckbot.db import Database
from nltk.util import ngrams
from nltk.tokenize import word_tokenize


class PullHistory(commands.Cog):
    def __init__(self, bot: DuckBot, db: Database):
        self.bot = bot
        self.db = db

    @commands.max_concurrency(number=1)
    @commands.guild_only()
    @commands.command(name="markovinit")
    async def markov_init_command(self, context, user: Member):
        channels = [c for c in self.bot.get_all_channels() if c.type == ChannelType.text]
        for channel in channels:
            async for message in channel.history().filter(lambda msg: msg.author == user):
                print(message)

    async def fetch_batch(self, channel: TextChannel, user: Member, before: Optional[Message] = None):
        count = 0
        messages = []
        async for message in channel.history(limit=1000, before=before):
            count += 1
            if not message.content.startswith(self.bot.command_prefix) and message.author == user:
                messages.append(message)
        return messages, count == 1000

    async def store_batch(self, messages: List[Message], user: Member):
        pass
        # words = word_tokenize()
        # grams2 = ngrams(
