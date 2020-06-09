import discord
import json
import random
from discord.ext import commands
from discord.utils import get

client = discord.Client()
client = commands.Bot(command_prefix = '!')


@client.event
async def on_ready():
	await client.change_presence(status = discord.Status.online, activity = discord.Game('Executing Muzz'))
	print('Bot is ready')


#Method for obtaining random quote from JSON file
def randomQuote():

	f = open('json.json')

	data = json.load(f)

	response = ''
	number = random.randint(0, len(data['messages'])) #Generates a random number to the length of the quotes
	response = str(data['messages'][number]['content']) #Finds the quote
	

	while len(response) < 8: #If the response is a short quote of less than 8 characters, try again
		
		if len(response) == 0: #If the response is blank (i.e. there is only an image)
			response = str(data['messages'][number]['attachments'][0]['url']) #Pull up the url of the image and post that
		else:
			number = random.randint(0, len(data['messages'])) 
			response = str(data['messages'][number]['content'])

	return (response)


@client.command()
async def quote(ctx):
	await ctx.send(randomQuote())

@client.command()
async def update(ctx):
	await ctx.send('Last updated on 06-08-2020')

@client.command()
async def creator(ctx):
	await ctx.send('Created by Jon Doucette')


@client.event
async def on_message(message):
	if message.author.id == 219308580036280321:
		await message.add_reaction('\u2753')

	await client.process_commands(message)

client.run('NzE1ODExMjE3OTAxNjE3MTUy.Xt8P_w.fLQqsCXf8W9-4WhbtbOXBHroBGY')

