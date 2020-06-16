import discord
import time
from discord.ext import commands


class Example(commands.Cog):

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
	@commands.command()
	async def ping(self, ctx):
		embed = discord.Embed(title = "Heres title 1")

		message = await ctx.send(embed = embed)

		for i in range(0,5):
			embed = discord.Embed(title = 'Heres title ' + str(i))
			time.sleep(.5)
			await message.edit(embed = embed)


		await ctx.send('Pong')

def setup(client):
	client.add_cog(Example(client))