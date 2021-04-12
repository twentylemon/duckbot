from .kubernetes import Kubernetes as Cog


def setup(bot):
    bot.add_cog(Cog(bot))
