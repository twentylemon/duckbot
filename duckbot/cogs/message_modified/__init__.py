from .message_modified import MessageModified


def setup(bot):
    bot.add_cog(MessageModified(bot))
