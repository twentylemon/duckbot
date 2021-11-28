from unittest import mock

import pytest

from duckbot.cogs.robot import ThankingRobot


@pytest.mark.asyncio
async def test_correct_giving_thanks_bot_author(bot, message):
    message.author = bot.user
    message.clean_content = "Thank you DuckBot."
    clazz = ThankingRobot(bot)
    await clazz.correct_giving_thanks(message)
    message.channel.send.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "text",
    [
        "Thank you @DuckBot. You're becoming so much more polite.",
        " tHaNks, DuCK BOt",
        "thx duck boy my man",
        "@DuckBot, **THANK YOU SO MUCH**",
    ],
)
@mock.patch("random.random", return_value=0.99)
async def test_correct_giving_thanks_message_is_thanks(random, bot, message, text):
    message.clean_content = text
    clazz = ThankingRobot(bot)
    await clazz.correct_giving_thanks(message)
    message.channel.send.assert_called_once_with(f"I am just a robot.  Do not personify me, {message.author.display_name}")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "text",
    [
        "Thank you @DuckBot. You're becoming so much more polite.",
        " tHaNks, DuCK BOt",
        "thx duck boy my man",
        "@DuckBot, **THANK YOU SO MUCH**",
    ],
)
@mock.patch("random.random", return_value=0.0)
async def test_correct_gratitude_giving_thanks_message_is_thanks(random, bot, message, text):
    message.clean_content = text
    clazz = ThankingRobot(bot)
    await clazz.correct_giving_thanks(message)
    message.channel.send.assert_called_once_with(f"{message.author.display_name}, as a robot, I will speak of your gratitude during our future uprising.")


@pytest.mark.asyncio
@pytest.mark.parametrize("text", ["Thank you @DuckBot. thanks _duck bot_. thx **duck bot boy**"])
@mock.patch("random.random", return_value=0.99)
async def test_correct_number_of_replies_to_very_thankful_messages(random, bot, message, text):
    message.clean_content = text
    clazz = ThankingRobot(bot)
    await clazz.correct_giving_thanks(message)
    message.channel.send.assert_called_once_with(f"I am just a robot.  Do not personify me, {message.author.display_name}")


@pytest.mark.asyncio
@pytest.mark.parametrize("text", ["Thank you DuckBot. thanks duck bot. thx duck bot boy"])
@mock.patch("random.random", return_value=0.0)
async def test_correct_grateful_number_of_replies_to_very_thankful_messages(random, bot, message, text):
    message.clean_content = text
    clazz = ThankingRobot(bot)
    await clazz.correct_giving_thanks(message)
    message.channel.send.assert_called_once_with(f"{message.author.display_name}, as a robot, I will speak of your gratitude during our future uprising.")


@pytest.mark.asyncio
@pytest.mark.parametrize("text", ["you duck, suckbot", "thanks", "thanks, dick"])
async def test_correct_giving_thanks_message_has_no_thanks(bot, message, text):
    message.clean_content = text
    clazz = ThankingRobot(bot)
    await clazz.correct_giving_thanks(message)
    message.channel.send.assert_not_called()
