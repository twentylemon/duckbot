import pytest
import mock
from tests.cog_test_ext import assert_cog_added
from discord.ext.commands import Bot
from duckbot.cogs.duck import setup as extension_setup, Duck


@pytest.mark.asyncio
async def test_setup():
    bot = mock.Mock(wraps=Bot(command_prefix=".", help_command=None))
    extension_setup(bot)
    await bot.close()
    assert_cog_added(bot, Duck)
