from .who_can_it_be_now import WhoCanItBeNow as Cog


def setup(bot):
    bot.add_cog(Cog(bot))
