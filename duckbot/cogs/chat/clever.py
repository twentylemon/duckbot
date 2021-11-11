import asyncio

from discord.ext import commands

from .session import Session


class Clever(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conversations = {}

    @commands.command(name="chat")
    async def chat_command(self, context):
        await self.chat(context)

    async def chat(self, context):
        if context.author.id in self.conversations:
            await self.stop_chat(context)
        else:
            await self.start_chat(context)

    async def start_chat(self, context):
        async with context.typing():
            session = Session()
            session.start()
            await context.send("My bindu is rady.")

        def session_check(message):
            return message.author.id == context.author.id

        self.conversations[context.author.id] = {"session": session}
        try:
            while True:
                task = self.bot.loop.create_task(self.bot.wait_for("message", check=session_check, timeout=60))
                self.conversations[context.author.id]["task"] = task
                try:
                    message = await task
                except asyncio.TimeoutError:
                    await context.send("timed out")
                    break
                except asyncio.CancelledError:
                    break
                async with context.typing():
                    response = await session.chat(message.content)
                    await message.reply(response, mention_author=False)
        finally:
            session.stop()
            del self.conversations[context.author.id]

    async def stop_chat(self, context):
        chat = self.conversations[context.author.id]
        chat["session"].stop()
        chat["task"].cancel()
