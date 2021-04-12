from .duck import Duck as Cog


def setup(bot):
    bot.add_cog(Cog(bot))
