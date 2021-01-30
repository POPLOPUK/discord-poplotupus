
class MainCog:
    def __init__(self, bot):
        self.bot = bot

    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            await ctx.send('You do not have the correct role for this command.')

def setup(bot):
    bot.add_cog(MainCog(bot))
