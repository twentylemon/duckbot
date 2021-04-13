from .announce_day import AnnounceDay


def setup(bot):
    print("here")
    bot.add_cog(AnnounceDay(bot))
