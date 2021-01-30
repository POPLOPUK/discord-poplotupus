from discord.ext import commands
import pickle
import random


class QuotesCog(commands.Cog, name='quotes'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="resetquotes", help="[Admin] Resets quote file during dev", parent="quotes")
    @commands.has_role("Admin")
    async def reset_quotes(self, ctx):
        try:
            file_handler = open('quotes.pkl', 'rb')
            quotes = pickle.load(file_handler)
            file_handler.close()
            file_handler = open('quotes_backup.pkl', 'wb')
            pickle.dump(quotes, file_handler)
            file_handler.close()
            quotes = {}
            file_handler = open('quotes.pkl', 'wb')
            pickle.dump(quotes, file_handler)
            file_handler.close()
            await ctx.send("Backup created. Quotes file reset")
        except:
            quotes = {}
            file_handler = open('quotes.pkl', 'wb')
            pickle.dump(quotes, file_handler)
            file_handler.close()
            await ctx.send("No backup created. Quotes file reset")
        await ctx.send("Done!")

    @commands.command(name="quote", help="quotes of various users in the server", parent="quotes")
    async def quote(self, ctx, name):
        file_handler = open('quotes.pkl', 'rb')
        quotes = pickle.load(file_handler)
        file_handler.close()
        try:
            msg = random.choice(quotes[name.lower()])
        except KeyError:
            msg = "That person does not have any quotes. check if you wrote it correctly "
        await ctx.send(msg)

    @commands.command(name="addquote", help="adds a quote to person", parent="quotes")
    async def add_quote(self, ctx, name, quote):
        file_handler = open('quotes.pkl', 'rb')
        quotes = pickle.load(file_handler)
        file_handler.close()
        try:
            quotes[name.lower()].append(str(quote))
        except KeyError:
            quotes[name.lower()] = [str(quote)]
        file_handler = open('quotes.pkl', 'wb')
        pickle.dump(quotes, file_handler)
        file_handler.close()

        await ctx.send("Cool added: \"" + str(quote) + "\" to " + name + "'s quotes")

    @commands.command(name="allquotes", help="displays all quotes of a person", parent="quotes")
    async def diplay_all_quotes(self, ctx, name):
        file_handler = open('quotes.pkl', 'rb')
        quotes = pickle.load(file_handler)
        file_handler.close()
        try:
            all_quotes = quotes[name]
            msg = ""
            for x in range(len(all_quotes)):
                msg = msg + all_quotes[x] + "\n"
            await ctx.send(msg)
        except KeyError:
            await ctx.send("That user does not exist")

    @commands.command(name="removequote", help="removes  a quote from a person", parent="quotes")
    async def remove_quote(self, ctx, name, quote):
        file_handler = open('quotes.pkl', 'rb')
        quotes = pickle.load(file_handler)
        file_handler.close()
        try:
            for x in range(len(quotes[name])):
                if quotes[name][x] == quote:
                    quotes[name].pop(x)
                    await ctx.send("Removed the quote")
                    file_handler = open('quotes.pkl', 'wb')
                    pickle.dump(quotes, file_handler)
                    file_handler.close()
                    return
            await ctx.send("Can't find that quote")
        except KeyError:
            await ctx.send("Can't find that user")


def setup(bot):
    bot.add_cog(QuotesCog(bot))
