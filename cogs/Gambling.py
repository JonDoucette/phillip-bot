import discord
import ezsheets
import random
from discord.ext import commands

"""
--------TO DO LIST-----------
Write the !bet command
Add in the !bet command error format
Come up with the !daily for credits
SlotMachine
Leaderboards
Create a shop system: Crates for xp and credits
Level system

"""

STARTING_CREDITS = 5000
STARTING_CRATES = 0
STARTING_EXP = 0
STARTING_LEVEL = 1

BET_PAYOUT = 2



class Gambling(commands.Cog):

	def __init__(self, client):
		self.client = client

	#Events
	@commands.Cog.listener()
	async def on_ready(self):
		print('Gambling Cog loaded')

#	@commands.Cog.listener()
#	async def on_message(self, message):
#		await message.add_reaction('\u2753') #Question Mark Unicode





	#Commands
	@commands.command()
	@commands.cooldown(1, 25, commands.BucketType.user)
	async def bet(self, ctx, amount = None, choice = None):

		"""
		DONE - Add checks to see if the user sent in an amount and choice


		DONE - Go to spreadsheet, find if user exists, if user doesn't add them in.
		DONE - Read the users credits, compare to the bet.
		DONE - If bet is possible, continue with bet


		DONE - Roll dice (1-10): 1-5 is low, 6-10 is high
		Done - Payout double the entry fee
		Done - Return number rolled, return response,
		Done - return loss/gain, return final credit balance fee

		COLUMNS:
		1 - ID
		2 - MMR
		3 - Name
		5 - Credits
		6 - Crates
		7 - EXP
		8 - Level
		"""

		author = ctx.message.author

		def choice_check(m):
			if m.author == ctx.author:
				if m.content.lower() == '!high' or m.content.lower() == '!low':
					return True
				else:
					return False
			else:
				return False

		if amount == None and choice == None:
			embed = discord.Embed(color = 0x607d8b)
			embed.add_field(name = 'Help', value = 'Guess if number is high or low\n (low = 1-5, high = 6-10)', inline = False)
			embed.add_field(name = 'Payout', value = '2x your bet', inline = False)
			embed.add_field(name = 'Usage', value = '**!bet <amount> <guess>**')
			await ctx.send(embed = embed)
		elif not amount.isdigit():
			await ctx.send('Please enter a bet amount.')
		elif choice == None:
			await ctx.send('Guess if the number is **!high** or **!low**')
			try:
				msg = await self.client.wait_for('message', check=choice_check, timeout=10)
			except asyncio.TimeoutError:
				return await ctx.send('Sorry, you took too long to answer.')
			choice = msg.content[1:]
			



		ss = ezsheets.Spreadsheet('14YXEduQ02xnWR7oB9tPpeCpoogPI-YwS9ycwNODxD68') #Opens up the google spreadsheets 'Tilted'
		sheet = ss['output']

		
		user = author.id
		user = str(user)

		amount = int(amount)
		
		if user in sheet.getColumn(1):
			location = sheet.getColumn(1).index(user)
			location += 1
			credits = sheet[5, location]

			if credits == '':
				credits = STARTING_CREDITS
			else:
				credits = int(credits)

		else:
			empty = sheet.getColumn(1).index('')
			location = empty + 1
			sheet[1, location] = user
			sheet[3, location] = author.name
			credits = sheet[5, location] = STARTING_CREDITS
			crates 	= sheet[6, location] = STARTING_CRATES
			xp 		= sheet[7, location] = STARTING_EXP
			level 	= sheet[8, location] = STARTING_LEVEL


		if amount > credits:
			await ctx.send(author.mention + ", you don't have enough credits.\n You have " + str(credits) + ' credits.')
		else:
			dice = random.randint(1,10)
			
			if dice < 6:
				roll = 'low'
			else:
				roll = 'high'

			if choice.lower() == roll: #If the user guesses correctly
				profit = amount
				credits += profit

				sheet[5, location] = credits

				embed = discord.Embed(color = 3066993, title = f'User: {author.name}')
				embed.add_field(name='Correct!', value = f'Number was **{dice}**', inline = True)
				embed.add_field(name='Profit', value = f'**{profit:,d}** credits', inline = True)
				embed.add_field(name='Credits', value = f'You have {credits:,d} credits', inline = False)

			else:
				profit = 0 - amount
				credits += profit

				sheet[5, location] = credits

				embed = discord.Embed(color = 0xFF0000, title = f'User: {author.name}')
				embed.add_field(name='Incorrect!', value = f'Number was **{dice}**', inline = True)
				embed.add_field(name='Profit', value = f'**{profit:,d}** credits', inline = True)
				embed.add_field(name='Credits', value = f'You have {credits:,d} credits', inline = False)



			await ctx.send(embed = embed)

	@commands.command(aliases = ['credit'])
	async def credits(self, ctx):
		author = ctx.message.author
		ss = ezsheets.Spreadsheet('14YXEduQ02xnWR7oB9tPpeCpoogPI-YwS9ycwNODxD68') #Opens up the google spreadsheets 'Tilted'
		sheet = ss['output']
		user = author.id
		user = str(user)

		#If the user exists
		if user in sheet.getColumn(1):
			location = sheet.getColumn(1).index(user)
			location += 1
			credits = sheet[5, location]

			if credits == '':
				credits = STARTING_CREDITS
			else:
				credits = int(credits)
		#If the user doesn't exist yet
		else:
			empty = sheet.getColumn(1).index('')
			location = empty + 1
			sheet[1, location] = user
			sheet[3, location] = author.name
			credits = sheet[5, location] = STARTING_CREDITS
			crates 	= sheet[6, location] = STARTING_CRATES
			xp 		= sheet[7, location] = STARTING_EXP
			level 	= sheet[8, location] = STARTING_LEVEL

		await ctx.send(author.mention + f', you have {credits:,d} credits.')






	### TO DO ###
	@bet.error
	async def bet_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			embed = discord.Embed(color = 0x607d8b, description = 'Please @ a specific user.')
			await ctx.send(embed = embed)
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.send(error)






def setup(client):
	client.add_cog(Gambling(client))