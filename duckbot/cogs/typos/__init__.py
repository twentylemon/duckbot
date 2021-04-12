from .typos import Typos as Cog


def setup(bot):
    bot.add_cog(Cog(bot))
