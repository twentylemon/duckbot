from .kubernetes import Kubernetes


def setup(bot):
    bot.add_cog(Kubernetes(bot))
