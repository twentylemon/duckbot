from .ascii_art import AsciiArt
import duckbot.cogs.text.markov


def setup(bot):
    bot.add_cog(AsciiArt(bot))
    bot.load_extension(duckbot.cogs.text.markov.__name__)
