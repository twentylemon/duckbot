from .insights import Insights as Cog


def setup(bot):
    bot.add_cog(Cog(bot))
