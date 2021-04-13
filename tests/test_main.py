import sys
import mock
from unittest.mock import call
import duckbot
from duckbot.__main__ import run_duckbot


@mock.patch("discord.ext.commands.Bot")
@mock.patch("discord.ext.tasks.Loop")
def test_duckbot_connection_test(bot, loop):
    with mock.patch.object(sys, "argv", ["connection-test"]):
        run_duckbot(bot)
        bot.load_extension.assert_any_call(duckbot.util.connection_test)
        bot.run.assert_called()


@mock.patch("discord.ext.commands.Bot")
@mock.patch("discord.ext.tasks.Loop")
def test_duckbot_normal_run(bot, loop):
    run_duckbot(bot)
    bot.run.assert_called()
