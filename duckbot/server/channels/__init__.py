from .channels import Channels


def setup(bot):
    bot.add_cog(Channels(bot))
