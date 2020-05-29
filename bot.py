import discord
import json
import random

client = discord.Client()

def randomQuote():

	f = open('json.json')

	data = json.load(f)

	response = ''

	while len(response) < 8:
		number = random.randint(0, len(data['messages']))
		response = str(data['messages'][number]['content'])

	return (response)


@client.event
async def on_message(message):
	if message.content.find("!quote") != -1:
		await message.channel.send(randomQuote())

	if message.content.find("!update") != -1:
		await message.channel.send('Last updated on 5-29-2020')


client.run('NzE1ODExMjE3OTAxNjE3MTUy.XtCpSA.AgiLs1GN8JbPzUCcKnIp6Qk7bWs')

