import pytest
from tests.cog_test_ext import assert_cog_added
from duckbot.cogs.audio import setup as extension_setup, WhoCanItBeNow


@pytest.mark.asyncio
async def test_setup(bot):
    extension_setup(bot)
    assert_cog_added(bot, WhoCanItBeNow)
