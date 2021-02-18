from discord.ext import commands
import lavalink
import discord
from discord import Embed
import re
import asyncio

url_rx = re.compile(r'https?://(?:www\.)?.+')

"""
Implemented bit of code from: https://github.com/Devoxin/Lavalink.py/blob/master/examples/music.py
"""


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        if not hasattr(self.bot, 'lavalink'):
            self.bot.music = lavalink.Client(self.bot.user.id)
            self.bot.music.add_node('127.0.0.1', 7000, 'testing', 'eu',
                                    'local_music_node')  # PASSWORD HERE MUST MATCH YML
            self.bot.add_listener(self.bot.music.voice_update_handler, 'on_socket_response')
        self.bot.music.add_event_hook(self.track_hook)

    @commands.command(name='play', alias=['p'],
                      help=".play {song name} to play a song, will connect the bot.")  # Allows for a song to be
    # played, does not make sure people are in the same chat.
    async def play_song(self, ctx, *, query: str):
        member = ctx.author  # warning person can call command anywhere.
        if member.voice is not None:
            vc = member.voice.channel
            player = self.bot.music.player_manager.create(ctx.guild.id)

            if not player.is_connected:
                player.store('channel', ctx.channel.id)  # used so we have the ctx.channel usage
                await self.connect_to(ctx.guild.id, str(vc.id))

            if player.is_connected and not ctx.author.voice.channel.id == int(
                    player.channel_id):  # Make sure the person is in the same channel as the bot to add to queue.
                return await ctx.channel.send("Please connect to the same chat as the bot.")

            try:
                query = query.strip('<>')
                if not url_rx.match(query):  # This and the line above and below allow for direct link play
                    query = f'ytsearch:{query}'

                results = await player.node.get_tracks(query)
                if not results or not results['tracks']:
                    return await ctx.send('Nothing found!')
                embed = discord.Embed(color=discord.Color.blurple())

                if results['loadType'] == 'PLAYLIST_LOADED':
                    tracks = results['tracks']

                    for track in tracks:
                        # Add all of the tracks from the playlist to the queue.
                        player.add(requester=ctx.author.id, track=track)

                    embed.title = 'Playlist Enqueued!'
                    embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'
                else:
                    track = results['tracks'][0]
                    embed.title = 'Track Enqueued'
                    embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'

                    # You can attach additional information to audiotracks through kwargs, however this involves
                    # constructing the AudioTrack class yourself.
                    track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
                    player.add(requester=ctx.author.id, track=track)
                # embed.set_author(str(ctx.author.id),ctx.author., ctx.author.avatar_url) idk why you no work

                await ctx.send(embed=embed)

                if not player.is_playing:
                    await player.play()
                    await player.set_volume(int(90))  # bot seems to clip at default 100 volume.
                """ old code
                try:
                    track = results['tracks'][0]
                    player.add(requester=ctx.author.id, track=track)
                    track_title = track["info"]["title"]
                    if not player.is_playing:
                        await player.play()
                        await player.set_volume(int(90))
                    await ctx.channel.send(f"{track_title} added to queue.")
                except Exception as error:
                    await ctx.channel.send("Song not found. (or title has emojis/symbols)")
                """
            except Exception as error:
                print(error)
        else:
            await ctx.channel.send("Please connect to a voice chat first.")

    async def track_hook(self, event):  # disconnects bot when song list is complete.
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            guild = self.bot.get_guild(guild_id)
            await guild.change_voice_state(channel=None)

    async def connect_to(self, guild_id: int, channel_id: str):
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

    @commands.command(name='skip', alias=["s"],
                      help="Skips currently playing song.")  # skips currently playing song
    async def skip_song(self, ctx, amount=1):
        try:
            player = self.bot.music.player_manager.get(ctx.guild.id)
            x = 0
            while x < amount:
                x = x + 1
                if ctx.author.voice is not None and ctx.author.voice.channel.id == int(player.channel_id):
                    if not player.is_playing:
                        return await ctx.channel.send("Nothing playing to skip.")
                    else:
                        await player.skip()
                        if x == 1:  # make sure song skipped only prints once.
                            await ctx.channel.send("Song skipped.")
                else:
                    return await ctx.channel.send("Please join the same voice channel as me.")
        except:
            return await ctx.channel.send("Nothing playing.")

    @commands.command(name="clear",
                      help="Clears all of the currently playing songs and makes the bot disconnect.")
    async def clear_queue(self, ctx):
        try:
            player = self.bot.music.player_manager.get(ctx.guild.id)
            if ctx.author.voice is not None and ctx.author.voice.channel.id == int(player.channel_id):
                if player.is_playing:
                    while player.is_playing:
                        await player.skip()
                    await ctx.channel.send("Songs Cleared.")
                else:
                    await ctx.channel.send("Nothing playing to clear.")
            else:
                await ctx.channel.send("Please join the same voice channel as me.")
        except:
            await ctx.channel.send("Nothing playing.")

    @commands.command(name='volume', aliases=['vol'])
    async def set_volume(self, ctx, volume: int = None):
        player = self.bot.music.player_manager.get(ctx.guild.id)
        if not volume:
            return await ctx.send(f"Current volume: {player.volume}%")  # return skips running code below
        await player.set_volume(int(volume))
        await ctx.channel.send(f"Volume set to {volume}%")

    # may remove this as it is depricated by clear, a safer alternative.
    @commands.command(name='disconnect', aliases=['dc'],
                      help="Force disconnects the bot from a voice channel")  # bad practice, better to use clear.
    async def disconnect_bot(self, ctx):
        player = self.bot.music.player_manager.get(ctx.guild.id)
        if not player.is_connected:
            return await ctx.channel.send("No bot is connected.")
        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.channel.send("Please join the same voice channel as me.")
        player.queue.clear()
        await player.stop()
        await ctx.guild.change_voice_state(channel=None)
        await ctx.channel.send("Bot disconnected.")

    @commands.command(name='pause', aliases=["ps"],
                      help="Pauses a song if one is playing.")  # command to pause currently playing music
    async def pause_bot(self, ctx):
        try:
            player = self.bot.music.player_manager.get(ctx.guild.id)
            if ctx.author.voice is not None and ctx.author.voice.channel.id == int(player.channel_id):
                if player.is_playing:
                    status = True
                    await ctx.channel.send("Song has been paused.")
                    await player.set_pause(True)
                    i = 0
                    while i < 84:  # This will periodically check to see if it has been unpaused
                        await asyncio.sleep(5)
                        i = i + 1
                        if not player.paused:  # If its been unpaused no need to keep counting. (Also fixes some issues)
                            status = False
                            break

                    if player.paused and player.is_playing and status is True:
                        await player.set_pause(False)  # If paused unpause.
                        await ctx.channel.send("Automatically unpaused.")

                else:
                    await ctx.channel.send("No song is playing to be paused.")
            else:
                await ctx.channel.send("Please join the same voice channel as me.")
        except:
            await ctx.channel.send("Nothing playing.")

    @commands.command(name='unpause', aliases=['resume', 'start', 'up'],
                      help="Unpauses a paused song.")  # command to unpause currently paused music
    async def unpause_bot(self, ctx):
        try:
            player = self.bot.music.player_manager.get(ctx.guild.id)
            if ctx.author.voice.channel.id == int(player.channel_id):
                if player.paused:
                    await ctx.channel.send("Resuming song.")
                    await player.set_pause(False)
                else:
                    await ctx.channel.send("Nothing is paused to resume.")
            else:
                await ctx.channel.send("Please join the same voice channel as me.")
        except:
            await ctx.channel.send("Nothing playing.")

    @commands.command(name='queue', aliases=['playlist', 'songlist', 'upnext', "q"],
                      help='Shows songs up next in order, with the currently playing at the top.')
    # display the songs in the order they are waiting to play
    async def queue(self, ctx, page=1):
        if not isinstance(page, int):  # Stop here if the page is not a valid number (save processing time).
            return ctx.channel.send("Please enter a valid number.")

        player = self.bot.music.player_manager.get(ctx.guild.id)
        if player.is_playing:
            songlist = player.queue
            list_collection = []
            complete_list = ''
            complete_list = complete_list + "NP: " + player.current['title'] + "\n"
            i = 0
            for song in songlist:
                complete_list = complete_list + f"{i + 1}: {song['title']}\n"
                i = i + 1
                if i % 10 == 0:  # Break into pages of 10 and add to a collection
                    list_collection.append(complete_list)
                    complete_list = ''

            if i % 10 != 0 or i == 0:  # Check for the case where it is not a perfect multiple, add "half page" (<
                # 10) or if there is only one song playing
                list_collection.append(complete_list)

            selection = page - 1
            embed = Embed()
            # add an inital if to check if it is an int then do page -1 if its not int default to page 0
            if int(selection) < 0:  # handle negative number
                list_collection[0] += "Page: 1/" + str(len(list_collection))
                embed.description = list_collection[0]
            elif int(selection) > len(list_collection) - 1:  # Handle a case where the index is greater than page amount
                list_collection[len(list_collection) - 1] += "Page: " + str(len(list_collection)) + "/" + str(
                    len(list_collection))
                embed.description = list_collection[len(list_collection) - 1]
            else:  # Handle a valid input case.
                list_collection[selection] += "Page: " + str(page) + "/" + str(len(list_collection))
                embed.description = list_collection[selection]
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("Nothing is queued.")

    @commands.command(name="shuffle", help="Indefinetely shuffles the songs to be played.")
    async def shuffle(self, ctx):
        try:
            player = self.bot.music.player_manager.get(ctx.guild.id)
            if ctx.author.voice is not None and ctx.author.voice.channel.id == int(player.channel_id):
                if player.is_playing:
                    try:
                        player.shuffle = True
                        await ctx.channel.send("Currently playing has been shuffled.")
                    except Exception as error:
                        print(error)
                else:
                    await ctx.channel.send("No music playing.")
            else:
                await ctx.channel.send("Please join my channel to shuffle.")
        except:
            await ctx.channel.send("Nothing playing.")


def setup(bot):
    bot.add_cog(Music(bot))
