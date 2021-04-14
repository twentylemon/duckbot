import os
import sys
from types import ModuleType
from discord.ext import commands
import duckbot.db
import duckbot.health
import duckbot.server.channels
import duckbot.server.emojis
import duckbot.cogs.duck
import duckbot.cogs.tito
import duckbot.cogs.audio
import duckbot.cogs.typos
import duckbot.cogs.robot
import duckbot.cogs.recipe
import duckbot.cogs.weather
import duckbot.cogs.bitcoin
import duckbot.cogs.insights
import duckbot.cogs.kubernetes
import duckbot.cogs.announce_day
import duckbot.cogs.message_modified
import duckbot.util.connection_test


def run_duckbot(bot: commands.Bot):
    if "connection-test" in sys.argv:
        bot.load_extension(duckbot.util.connection_test.__name__)

    bot.load_extension(duckbot.health.__name__)

    bot.load_extension(duckbot.db.__name__)

    # server cogs must be loaded first; any references to
    # them should happen in or after the `on_ready` event
    bot.load_extension(duckbot.server.channels.__name__)
    bot.load_extension(duckbot.server.emojis.__name__)

    bot.load_extension(duckbot.cogs.duck.__name__)
    bot.load_extension(duckbot.cogs.tito.__name__)
    bot.load_extension(duckbot.cogs.audio.__name__)
    bot.load_extension(duckbot.cogs.typos.__name__)
    bot.load_extension(duckbot.cogs.robot.__name__)
    bot.load_extension(duckbot.cogs.recipe.__name__)
    bot.load_extension(duckbot.cogs.weather.__name__)
    bot.load_extension(duckbot.cogs.bitcoin.__name__)
    bot.load_extension(duckbot.cogs.insights.__name__)
    bot.load_extension(duckbot.cogs.kubernetes.__name__)
    bot.load_extension(duckbot.cogs.announce_day.__name__)
    bot.load_extension(duckbot.cogs.message_modified.__name__)

    bot.run(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    bot = commands.Bot(command_prefix="!", help_command=None)
    run_duckbot(bot)
