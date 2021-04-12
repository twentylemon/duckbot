from .emojis import Emojis


def setup(bot):
    bot.add_cog(Emojis(bot))
