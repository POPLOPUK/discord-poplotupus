from discord.ext import commands
import discord
import pickle
import random
import aiohttp
import io


class SoundMediaCog(commands.Cog, name='media'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="resetsound", help="[Admin] Resets drawing file during dev", parent="drawings")
    @commands.has_role("Admin")
    async def reset_sounds(self, ctx):
        try:
            file_handler = open('sounds.pkl', 'rb')
            drawings = pickle.load(file_handler)
            file_handler.close()
            file_handler = open('sounds_backup.pkl', 'wb')
            pickle.dump(drawings, file_handler)
            file_handler.close()
            drawings = {}
            file_handler = open('sounds.pkl', 'wb')
            pickle.dump(drawings, file_handler)
            file_handler.close()
            await ctx.send("Backup created. sound file reset")
        except:
            drawings = {}
            file_handler = open('sounds.pkl', 'wb')
            pickle.dump(drawings, file_handler)
            file_handler.close()
            await ctx.send("No backup created. sound file reset")
        await ctx.send("Done!")

    @commands.command(name="addsound", help="add a sound file", parent="drawings")
    async def add_sound(self, ctx, name, link):
        file_handler = open('sounds.pkl', 'rb')
        sounds = pickle.load(file_handler)
        file_handler.close()
        sounds[name.lower()] = str(link)
        file_handler = open('sounds.pkl', 'wb')
        pickle.dump(sounds, file_handler)
        file_handler.close()
        await ctx.send("Cool added:")
        await ctx.send(str(link))
        await ctx.send("to " + name + "'s sounds")

    @commands.command(name="sound", help=".sound [name]. Sounds of *slam* ", parent="drawings")
    async def send_sound(self, ctx, name):
        file_handler = open('sounds.pkl', 'rb')
        sounds = pickle.load(file_handler)
        file_handler.close()
        url = sounds[name]
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        # print("test2")
                        return url
                    # print(resp.status)
                    # print("test")
                    data = io.BytesIO(await resp.read())
            await ctx.send(file=discord.File(data, (name + ".mp3")))
        except KeyError:
            msg = "There is not file with that sound"

    @commands.command(name="listsound", help="Displays all the sounds made by --jason-- everyone", parent="drawings")
    async def display_all_media(self, ctx):
        file_handler = open('sounds.pkl', 'rb')
        sound = pickle.load(file_handler)
        file_handler.close()
        keys = list(sound.keys())
        try:
            msg = ""
            for x in range(len(keys)):
                msg = msg + keys[x] + "\n"
            await ctx.send(msg)
        except KeyError:
            await ctx.send("That media does not exist")

def setup(bot):
    bot.add_cog(SoundMediaCog(bot))
