import discord
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
		await ctx.send('Pong')

def setup(client):
	client.add_cog(Example(client))