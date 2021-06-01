from .ascii_art import AsciiArt
from .markov import MarkovChain


def setup(bot):
    from duckbot.db import Database

    bot.add_cog(AsciiArt(bot))
    bot.add_cog(MarkovChain(bot, Database()))
