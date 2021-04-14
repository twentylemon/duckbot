import pytest
from tests.cog_test_ext import assert_cog_added
from duckbot.cogs.typos import setup as extension_setup, Typos


@pytest.mark.asyncio
async def test_setup(bot):
    extension_setup(bot)
    assert_cog_added(bot, Typos)
