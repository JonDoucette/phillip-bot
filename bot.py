import discord
import json
import random

client = discord.Client()


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

@client.event
async def on_message(message):
	if message.content.find("!quote") != -1:
		await message.channel.send(randomQuote())

	elif message.content.find("!update") != -1:
		await message.channel.send('Last updated on 06-01-2020')

	elif message.content.find("!creator") != -1:
		await message.channel.send('Created by Jon Doucette')

client.run('NzE1ODExMjE3OTAxNjE3MTUy.XtCpSA.AgiLs1GN8JbPzUCcKnIp6Qk7bWs')

