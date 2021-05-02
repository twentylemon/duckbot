from .clever import Clever


def setup(bot):
    bot.add_cog(Clever(bot))
