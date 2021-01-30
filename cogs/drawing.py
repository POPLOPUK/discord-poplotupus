from discord.ext import commands
import pickle


class DrawingsCog(commands.Cog, name='drawings'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="resetdrawings", help="[Admin] Resets drawing file during dev", parent="drawings")
    @commands.has_role("Admin")
    async def reset_drawings(ctx):
        try:
            file_handler = open('drawings.pkl', 'rb')
            drawings = pickle.load(file_handler)
            file_handler.close()
            file_handler = open('drawings_backup.pkl', 'wb')
            pickle.dump(drawings, file_handler)
            file_handler.close()
            drawings = {}
            file_handler = open('drawings.pkl', 'wb')
            pickle.dump(drawings, file_handler)
            file_handler.close()
        except:
            drawings = {}
            file_handler = open('drawings.pkl', 'wb')
            pickle.dump(drawings, file_handler)
            file_handler.close()

    @commands.command(name="adddrawing", help="adds a drawing to person", parent="drawings")
    async def add_drawing(ctx, name, link):
        file_handler = open('drawings.pkl', 'rb')
        drawings = pickle.load(file_handler)
        file_handler.close()
        try:
            drawings[name.lower()].append(str(link))
        except KeyError:
            drawings[name.lower()] = [str(link)]
        file_handler = open('drawings.pkl', 'wb')
        pickle.dump(drawings, file_handler)
        file_handler.close()
        await ctx.send("Cool added:")
        await ctx.send(str(link))
        await ctx.send("to " + name + "'s drawings")

    @commands.command(name="drawing", help="quotes of various users in the server", parent="drawings")
    async def send_drawing(ctx, name):
        file_handler = open('drawings.pkl', 'rb')
        drawings = pickle.load(file_handler)
        file_handler.close()
        try:
            msg = random.choice(drawings[name.lower()])
        except KeyError:
            msg = "That person does not have any drawings. check if you wrote it correctly "

        await ctx.send(msg)


def setup(bot):
    bot.add_cog(DrawingsCog(bot))
