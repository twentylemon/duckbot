from .pull_history import PullHistory


def setup(bot):
    from duckbot.db import Database

    bot.add_cog(PullHistory(bot, Database()))
