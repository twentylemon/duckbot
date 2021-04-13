from .message_edit_diff import MessageEditDiff


def setup(bot):
    bot.add_cog(MessageEditDiff(bot))
