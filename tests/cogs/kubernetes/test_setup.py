import pytest
import mock
from tests.cog_test_ext import assert_cog_added
from discord.ext.commands import Bot
from duckbot.cogs.kubernetes import setup as extension_setup, Kubernetes


@pytest.mark.asyncio
async def test_setup():
    bot = mock.Mock(wraps=Bot(command_prefix="."))
    extension_setup(bot)
    await bot.close()
    assert_cog_added(bot, Kubernetes)
