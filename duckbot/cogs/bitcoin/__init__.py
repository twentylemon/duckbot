from .bitcoin import Bitcoin


def setup(bot):
    bot.add_cog(Bitcoin(bot))
