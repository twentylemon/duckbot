from .recipe import Recipe as Cog


def setup(bot):
    bot.add_cog(Cog(bot))
