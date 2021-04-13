import os
import sys
from discord.ext import commands
import duckbot
import duckbot.db
import duckbot.health


def run_duckbot(bot: commands.Bot):
    if "connection-test" in sys.argv:
        bot.load_extension(duckbot.util.connection_test)

    bot.load_extension(duckbot.health)

    bot.load_extension(duckbot.db)

    # server cogs must be loaded first; any references to
    # them should happen in or after the `on_ready` event
    bot.load_extension(duckbot.server.channels)
    bot.load_extension(duckbot.server.emojis)

    bot.load_extension(duckbot.cogs.duck)
    bot.load_extension(duckbot.cogs.tito)
    bot.load_extension(duckbot.cogs.audio)
    bot.load_extension(duckbot.cogs.typos)
    bot.load_extension(duckbot.cogs.robot)
    bot.load_extension(duckbot.cogs.recipe)
    bot.load_extension(duckbot.cogs.bitcoin)
    bot.load_extension(duckbot.cogs.insights)
    bot.load_extension(duckbot.cogs.kubernetes)
    bot.load_extension(duckbot.cogs.announce_day)
    bot.load_extension(duckbot.cogs.message_modified)

    bot.run(os.getenv("DISCORD_TOKEN"))


if __name__ == "__main__":
    bot = commands.Bot(command_prefix="!", help_command=None)
    run_duckbot(bot)
