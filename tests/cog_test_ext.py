def assert_cog_added(bot, typ):
    """Asserts a cog of the given type was added to the bot."""
    called = False
    for invocation in bot.add_cog.call_args_list:
        if isinstance(invocation[0][0], typ):
            called = True
    if not called:
        bot.add_cog.assert_any_call(typ)
