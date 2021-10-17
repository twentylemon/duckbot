from typing import List, Optional, Union

import markovify
from discord import ChannelType, Member, Message, TextChannel, User
from discord.ext import commands
from nltk.tokenize import word_tokenize
from nltk.util import ngrams

from duckbot import DuckBot
from duckbot.db import Database


class PullHistory(commands.Cog):
    def __init__(self, bot: DuckBot, db: Database):
        self.bot = bot
        self.db = db

    @commands.max_concurrency(number=1)
    # @commands.guild_only()
    @commands.command(name="markovify")
    async def markovify_command(self, context, user: Union[User, Member]):
        channels = [c for c in self.bot.get_all_channels() if c.type == ChannelType.text]
        for channel in channels:
            messages, still_more = await self.fetch_batch(channel, user)
            content = ". ".join([x.clean_content for x in messages])
            model = markovify.Text(content)
            for i in range(10):
                print(model.make_sentence())

    @commands.max_concurrency(number=1)
    # @commands.guild_only()
    @commands.command(name="markovinit")
    async def markov_init_command(self, context, user: Union[User, Member]):
        channels = [c for c in self.bot.get_all_channels() if c.type == ChannelType.text]
        for channel in channels:
            messages, still_more = await self.fetch_batch(channel, user)
            await self.store_batch(messages, user)
            # async for message in channel.history().filter(lambda msg: msg.author == user):
            #     print(message)

    async def fetch_batch(self, channel: TextChannel, user: Member, before: Optional[Message] = None):
        count = 0
        messages = []
        async for message in channel.history(limit=1000, before=before):
            count += 1
            if not message.content.startswith(self.bot.command_prefix) and message.author == user:
                messages.append(message)
        return messages, count == 1000

    async def store_batch(self, messages: List[Message], user: Member):
        for message in messages:
            words = word_tokenize(message.clean_content)  # TODO remove markdown
            # words = message.clean_content.split()
            async for size in self.ngram_range():
                grams = ngrams(words, size)
                print([x for x in grams])

    async def ngram_range(self):
        for n in range(1, 4 + 1):
            yield n
