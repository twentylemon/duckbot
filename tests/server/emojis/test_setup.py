import pytest
from tests.cog_test_ext import assert_cog_added
from duckbot.util.connection_test import setup as extension_setup, ConnectionTest


@pytest.mark.asyncio
async def test_setup(bot):
    extension_setup(bot)
    assert_cog_added(bot, ConnectionTest)
