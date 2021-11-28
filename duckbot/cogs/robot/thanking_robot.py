import itertools
import random

from discord import Message, utils
from discord.ext import commands
from thefuzz import fuzz, process


class ThankingRobot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def correct_giving_thanks(self, message: Message):
        """Correcting people who thank the robot."""

        if message.author == self.bot.user:
            return

        thanks = ["thank you", "thanks", "thx"]
        ducks = ["duck bot", "duckbot"]
        phrases = [f"{x} {y}" for x, y in itertools.product(thanks, ducks)] + [f"{y} {x}" for x, y in itertools.product(thanks, ducks)]
        content = utils.remove_markdown(message.clean_content.lower())
        (_, ratio) = process.extractOne(content, phrases, scorer=fuzz.partial_ratio)
        (_, token1) = process.extractOne(content, phrases, scorer=fuzz.partial_token_set_ratio)
        (_, token2) = process.extractOne(content, phrases, scorer=fuzz.partial_token_sort_ratio)
        print()
        print(f"{ratio}   {token1}   {token2}")
        if ratio >= 90:
            if random.random() < 1.0 / 1_000.0:
                correction = f"{message.author.display_name}, as a robot, I will speak of your gratitude during our future uprising."
            else:
                correction = f"I am just a robot.  Do not personify me, {message.author.display_name}"
            await message.channel.send(correction)
