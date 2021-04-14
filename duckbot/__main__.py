import os
import sys
from types import ModuleType
from discord.ext import commands
import duckbot
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


def load_extension(bot: commands.Bot, mod: ModuleType):
    bot.load_extension(mod.__name__)


def run_duckbot(bot: commands.Bot):
    if "connection-test" in sys.argv:
        load_extension(bot, duckbot.util.connection_test)

    load_extension(bot, duckbot.health)

    load_extension(bot, duckbot.db)

    # server cogs must be loaded first; any references to
    # them should happen in or after the `on_ready` event
    load_extension(bot, duckbot.server.channels)
    load_extension(bot, duckbot.server.emojis)

    load_extension(bot, duckbot.cogs.duck)
    load_extension(bot, duckbot.cogs.tito)
    load_extension(bot, duckbot.cogs.audio)
    load_extension(bot, duckbot.cogs.typos)
    load_extension(bot, duckbot.cogs.robot)
    load_extension(bot, duckbot.cogs.recipe)
    load_extension(bot, duckbot.cogs.weather)
    load_extension(bot, duckbot.cogs.bitcoin)
    load_extension(bot, duckbot.cogs.insights)
    load_extension(bot, duckbot.cogs.kubernetes)
    load_extension(bot, duckbot.cogs.announce_day)
    load_extension(bot, duckbot.cogs.message_modified)

    bot.run(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    bot = commands.Bot(command_prefix="!", help_command=None)
    run_duckbot(bot)
