from .thanking_robot import ThankingRobot as Cog


def setup(bot):
    bot.add_cog(Cog(bot))
