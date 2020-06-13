import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os

class Voice(commands.Cog):

	def __init__(self, client):
		self.client = client

	#Events
	@commands.Cog.listener()
	async def on_ready(self):
		print('Example Cog Loaded')

#	@commands.Cog.listener()
#	async def on_message(self, message):
#		await message.add_reaction('\u2753') #Question Mark Unicode

	#Commands

	@commands.command(aliases=['j', 'joi'])
	async def join(self, ctx):
		channel = ctx.message.author.voice.channel
		voice = get(self.client.voice_clients, guild=ctx.guild)

		if voice and voice.is_connected():
			await voice.move_to(channel)
		else:
			voice = await channel.connect()
			print(f"The bot has connected to {channel}\n")

		await ctx.send(f"Joined {channel}")


	@commands.command(aliases=['l', 'lea'])
	async def leave(self, ctx):
		channel = ctx.message.author.voice.channel
		voice = get(self.client.voice_clients, guild=ctx.guild)

		if voice and voice.is_connected():
			await voice.disconnect()
			print(f"The bot has left {channel}")
			await ctx.send(f"Left {channel}")
		else:
			print("Bot was told to leave voice channel, but was not in one")
			await ctx.send("Don't think I am in a voice channel")



	@commands.command(aliases=['p', 'pla'])
	async def play(self, ctx, url: str):

		song_there = os.path.isfile("song.mp3")
		try:
			if song_there:
				os.remove("song.mp3")
				print("Removed old song file")
		except (PermissionError) as e:
				print("Trying to delete song file, but it's being played")
				await ctx.send("ERROR: Music playing")
				return

		await ctx.send("Getting everything ready now")

		channel = ctx.message.author.voice.channel
		voice = get(self.client.voice_clients, guild=ctx.guild)

		if voice and voice.is_connected():
			await voice.move_to(channel)
		else:
			voice = await channel.connect()
			print(f"The bot has connected to {channel}\n")

		await ctx.send(f"Joined {channel}")



		#voice = get(self.client.voice_clients, guild=ctx.guild)

		ydl_opts = {
	        'format': 'bestaudio/best',
	        'postprocessors': [{
	            'key': 'FFmpegExtractAudio',
	            'preferredcodec': 'mp3',
	            'preferredquality': '192',
	        }],
	    }

		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			print("Downloading audio now\n")
			ydl.download([url])

		for file in os.listdir("./"):
			if file.endswith(".mp3"):
				name = file
				print(f"Renamed File: {file}\n")
				os.rename(file, "song.mp3")

		voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
		voice.source = discord.PCMVolumeTransformer(voice.source)
		voice.source.volume = 0.5

		nname = name.rsplit("-", 2)
		await ctx.send(f"Playing: {nname[0]}")
		print("playing\n")

def setup(client):
	client.add_cog(Voice(client))