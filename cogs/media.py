from discord.ext import commands
import pickle


class MediaCog(commands.Cog, name='media'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="allmedia", help="[Admin] Resets drawing file during dev", parent="drawings")
    async def display_all_media(self, ctx):
        file_handler = open('media.pkl', 'rb')
        media = pickle.load(file_handler)
        file_handler.close()
        keys = list(media.keys())
        try:
            msg = ""
            for x in range(len(keys)):
                msg = msg + keys[x] + "\n"
            await ctx.send(msg)
        except KeyError:
            await ctx.send("That media does not exist")

    @commands.command(name="resetmedia", help="[Admin] Resets drawing file during dev", parent="drawings")
    @commands.has_role("Admin")
    async def reset_media(self, ctx):
        try:
            file_handler = open('media.pkl', 'rb')
            media = pickle.load(file_handler)
            file_handler.close()
            file_handler = open('media_backup.pkl', 'wb')
            pickle.dump(media, file_handler)
            file_handler.close()
            media = {}
            file_handler = open('media.pkl', 'wb')
            pickle.dump(media, file_handler)
            file_handler.close()
            await ctx.send("Backup created. Quotes file reset")
        except:
            media = {}
            file_handler = open('media.pkl', 'wb')
            pickle.dump(media, file_handler)
            file_handler.close()
            await ctx.send("No backup created. Quotes file reset")
        await ctx.send("Done!")

    @commands.command(name="addmedia", help="adds a gif/image", parent="drawings")
    async def add_media(self, ctx, media_name, link):
        file_handler = open('media.pkl', 'rb')
        media = pickle.load(file_handler)
        file_handler.close()
        media[media_name.lower()] = str(link)
        file_handler = open('media.pkl', 'wb')
        pickle.dump(media, file_handler)
        file_handler.close()
        await ctx.send("Cool added:")
        await ctx.send(str(link))
        await ctx.send("to " + media_name + "'s media")

    @commands.command(name="media", help="media shit", parent="drawings")
    async def send_media(self, ctx, media_name):
        file_handler = open('media.pkl', 'rb')
        media = pickle.load(file_handler)
        file_handler.close()
        await ctx.send(media[media_name.lower()])


def setup(bot):
    bot.add_cog(MediaCog(bot))
