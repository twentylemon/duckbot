import pytest
from tests.cog_test_ext import assert_cog_added
from duckbot.health import setup as extension_setup, HealthCheck


@pytest.mark.asyncio
async def test_setup(bot):
    extension_setup(bot)
    assert_cog_added(bot, HealthCheck)
