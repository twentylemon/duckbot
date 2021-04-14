import sys
import mock
from unittest.mock import call
import duckbot
from duckbot.__main__ import run_duckbot


def test_duckbot_connection_test(bot):
    with mock.patch.object(sys, "argv", ["connection-test"]):
        run_duckbot(bot)
        bot.load_extension.assert_any_call(duckbot.util.connection_test.__name__)
        bot.run.assert_called()


def test_duckbot_normal_run(bot):
    run_duckbot(bot)
    bot.run.assert_called()
