import pytest
from tests.cog_test_ext import assert_cog_added
from duckbot.cogs.message_modified import setup as extension_setup, MessageModified


@pytest.mark.asyncio
async def test_setup(bot):
    extension_setup(bot)
    assert_cog_added(bot, MessageModified)
