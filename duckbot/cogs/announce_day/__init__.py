from .announce_day import AnnounceDay as Cog


def setup(bot):
    bot.add_cog(Cog(bot))
