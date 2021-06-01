from .ascii_art import AsciiArt
from .markov_chain import MarkovChain


def setup(bot):
    from duckbot.db import Database

    bot.add_cog(AsciiArt(bot))
    bot.add_cog(MarkovChain(bot, Database()))
