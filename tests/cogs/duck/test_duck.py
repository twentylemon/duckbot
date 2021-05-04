import pytest
from unittest import mock
from duckbot.cogs.duck import Duck


@pytest.mark.asyncio
@mock.patch("random.random", return_value=0.0001)
async def test_react_duck_random_passes(random, message):
    clazz = Duck(None)
    await clazz.react_duck(message)
    message.add_reaction.assert_not_called()


@pytest.mark.asyncio
@mock.patch("random.random", return_value=0.000009)
async def test_react_duck_random_fails(random, message):
    clazz = Duck(None)
    await clazz.react_duck(message)
    message.add_reaction.assert_called_once_with("\U0001F986")


@pytest.mark.asyncio
async def test_github(context):
    clazz = Duck(None)
    await clazz._Duck__github(context)
    context.send.assert_called_once_with("https://github.com/Chippers255/duckbot")


@pytest.mark.asyncio
async def test_wiki(context):
    clazz = Duck(None)
    await clazz._Duck__wiki(context)
    context.send.assert_called_once_with("https://github.com/Chippers255/duckbot/wiki")