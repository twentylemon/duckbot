import pytest
from tests.cog_test_ext import assert_cog_added
from duckbot.cogs.announce_day import setup as extension_setup, AnnounceDay


@pytest.mark.asyncio
async def test_setup(bot):
    extension_setup(bot)
    assert_cog_added(bot, AnnounceDay)
