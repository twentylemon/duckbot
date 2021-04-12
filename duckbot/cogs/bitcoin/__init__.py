from .bitcoin import Bitcoin as Cog


def setup(bot):
    bot.add_cog(Cog(bot))
