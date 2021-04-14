import pytest
from tests.cog_test_ext import assert_cog_added
from duckbot.cogs.recipe import setup as extension_setup, Recipe


@pytest.mark.asyncio
async def test_setup(bot):
    extension_setup(bot)
    assert_cog_added(bot, Recipe)
