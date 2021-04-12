from .database import Database


def setup(bot):
    bot.add_cog(Database(bot))
