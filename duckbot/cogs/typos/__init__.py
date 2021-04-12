from .typos import Typos


def setup(bot):
    bot.add_cog(Typos(bot))
