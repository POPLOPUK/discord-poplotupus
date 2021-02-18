from discord.ext import commands


def botcommandscheck(m):
    botcommands = ["$w", "$im", "$k", "$wl", "$h", ".reboot", ".help", "$mu", "$mm", "$wa", "$ha", "$dk", "$daily",
                   "$rolls", "$wishlist", "y", "$ts", "$trade", "$give"]
    if int(m.author.id) == 432610292342587392:
        if m.content.lower().find("married") >= 0:
            return False
        elif m.content.lower().find("given") >= 0:
            return False
        elif m.content.lower().find("wished") >= 0:
            return False
        else:
            return True

    elif int(m.author.id) == 770077123662446642:
        return True
    elif int(m.author.id) == 705016654341472327:
        return True
    elif str(m.content.lower()) in botcommands:
        return True
    elif str(m.content.lower()).find("$im") >= 0:
        return True
    elif str(m.content.lower()).find(".cleanmsg") >= 0:
        return True
    elif str(m.content.lower()).find("$give") >= 0:
        return True
    elif str(m.content.lower()).find("p!") >= 0:
        return True
    elif str(m.content.lower()).find("$wish") >= 0:
        return True
    elif str(m.content.lower()).find("$divorce") >= 0:
        return True
    else:
        return False


def isChirag(m):
    return m.author.id == 178876861542039553


class ClearBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='cleanmsg')
    @commands.check(isChirag)
    async def cleanmsg(self, ctx, amount=1):
        try:
            t2 = await ctx.channel.purge(limit=amount, check=botcommandscheck)
            await ctx.channel.send(f"Deleted {len(t2)} messages")
        except:
            await ctx.channel.send("Error")


def setup(bot):
    bot.add_cog(ClearBot(bot))
