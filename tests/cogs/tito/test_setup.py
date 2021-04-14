import pytest
from tests.cog_test_ext import assert_cog_added
from duckbot.cogs.tito import setup as extension_setup, Tito


@pytest.mark.asyncio
async def test_setup(bot):
    extension_setup(bot)
    assert_cog_added(bot, Tito)
