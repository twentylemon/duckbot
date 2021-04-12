from .tito import Tito as Cog


def setup(bot):
    bot.add_cog(Cog(bot))
