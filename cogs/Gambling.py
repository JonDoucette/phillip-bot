import discord
import ezsheets
import random
import datetime
from discord.ext import commands

"""
--------TO DO LIST-----------
DONE - Write the !bet command
DONE - Add in the !bet command error format
DONE - Come up with the !daily for credits

TO DO NEXT - SlotMachine

!register command for new users, should make program run faster

DONE - Leaderboards
Create a shop system: Crates for xp and credits
Level system

Done - !search command to find 25 - 100 coins on ground
Done - Stats with games played, overall profit and profit based on game



!bet command and you go with the multiplier -NEED TO REWRUITE BET COMMAND FOR THIS I THINK

"""

STARTING_CREDITS = 5000
STARTING_CRATES = 0
STARTING_EXP = 0
STARTING_LEVEL = 1
DAILY_AMOUNT = 2500

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
	@commands.cooldown(1, 15, commands.BucketType.user)
	async def bet(self, ctx, amount = None, choice = None):
		"""
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
		elif choice.lower() != 'high' and choice.lower() != 'low':
			await ctx.send('Invalid betting choice. Next time use **!high** or **!low**.')
			return

			



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
		
		amount = int(amount)

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

			#Adds data to the statistics
			totalProf = int(sheet[9, location])
			totalProf += profit
			sheet[9, location] = totalProf

			gamesPlayed = int(sheet[10, location])
			gamesPlayed += 1
			sheet[10, location] = gamesPlayed

			highlowProfit = int(sheet[11, location])
			highlowProfit += profit
			sheet[11, location] = highlowProfit



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

	@commands.command(aliases = ['dailies'])
	@commands.cooldown(1, 86400, commands.BucketType.user)
	async def daily(self, ctx):
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

		credits += DAILY_AMOUNT
		sheet[5,location] = credits

		embed = discord.Embed(color = 3066993)
		embed.add_field(name = f'You got {DAILY_AMOUNT:,d} credits', value = f'You have {credits:,d} credits', inline = False)

		await ctx.send(embed = embed)

	@commands.command()
	async def search(self, ctx):
		ss = ezsheets.Spreadsheet('14YXEduQ02xnWR7oB9tPpeCpoogPI-YwS9ycwNODxD68') #Opens up the google spreadsheets 'Tilted'
		sheet = ss['output']
		author = ctx.message.author
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

		print(credits)

		if credits <= 25:
			rand = random.randint(25, 100)
			credits += rand
			sheet[5, location] = credits
			embed = discord.Embed(color = 3066993)
			embed.add_field(name = f'You have found {rand} credits.', value = f'You have {credits} credits.')			
		else:
			embed = discord.Embed(color = 0xFF0000, description = 'You can only search with 25 credits or less.')

		await ctx.send(embed = embed)



	@commands.command(aliases = ['leaderboards', 'leader', 'lead', 'leaders'])
	async def leaderboard(self, ctx):
		ss = ezsheets.Spreadsheet('14YXEduQ02xnWR7oB9tPpeCpoogPI-YwS9ycwNODxD68') #Opens up the google spreadsheets 'Tilted'
		sheet = ss['output']

		response = ''
		name = ''
		names = []

		creditList = sheet.getColumn(5)
		creditList[0] = 0
		removal = creditList.index('')
		removal -= 1
		del creditList[0]
		del creditList[removal:] #Removes all of the blank credits from the list
		creditList = list(map(int, creditList)) #Converts all items in the list to integer

		for i in range(5):
			amount = max(creditList)
			index = creditList.index(amount)
			
			for r in range(200):
				row = sheet.getRow(r+1)
				if str(amount) in row:
					name = sheet[3, (r+1)]
					
					if name in names:
						continue
					else:
						names.append(name)
						break

			response += f'{i+1}. {name:<10} - {amount:>10,d} credits\n'
			index = creditList.index(amount)

			del creditList[index]


		embed = discord.Embed(color = 0xffff00)
		embed.set_author(name = response)
		await ctx.send(embed = embed)

	@commands.command(aliases = ['loserboards', 'loser', 'lose', 'losers'])
	async def loserboard(self, ctx):
		ss = ezsheets.Spreadsheet('14YXEduQ02xnWR7oB9tPpeCpoogPI-YwS9ycwNODxD68') #Opens up the google spreadsheets 'Tilted'
		sheet = ss['output']

		response = ''
		name = ''
		names = []

		creditList = sheet.getColumn(5)
		creditList[0] = 0
		removal = creditList.index('')
		removal -= 1
		del creditList[0]
		del creditList[removal:] #Removes all of the blank credits from the list
		print(creditList)

		creditList = list(map(int, creditList)) #Converts all items in the list to integer

		for i in range(5):
			amount = min(creditList)
			index = creditList.index(amount)
			
			print(f'Index: {index}')


			for r in range(200):
				#row = sheet.getRow(r+1)
				row = sheet[5, (r+2)]
				print(row)
				if row in str(amount):
					name = sheet[3, (r+2)]
					
					print(f'Row: {r + 2}')
					
					if name in names:
						continue
					else:
						names.append(name)
						break




			response += f'{i+1}. {name:<10} - {amount:>10,d} credits\n'
			index = creditList.index(amount)

			del creditList[index]


		embed = discord.Embed(color = 0xffff00)
		embed.set_author(name = response)
		await ctx.send(embed = embed)

	@commands.command(aliases = ['stat'])
	async def stats(self, ctx):
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

		totalProf = int(sheet[9, location])
		gamesPlayed = int(sheet[10, location])
		betProfit = int(sheet[11, location])

		embed = discord.Embed(color = 0xffff00)
		embed.add_field(name = 'Total Profit', value = f'{totalProf:,d}', inline = True)
		embed.add_field(name = 'Games Played', value = f'{gamesPlayed}', inline = True)
		embed.add_field(name = 'High Low Profit', value = f'{betProfit:,d}', inline = True)
		embed.set_footer(text = f'You currently have {credits:,d} credits.')

		await ctx.send(embed = embed)










	### TO DO ###
	@bet.error
	async def bet_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			embed = discord.Embed(color = 0x607d8b, description = 'Please @ a specific user.')
			await ctx.send(embed = embed)
		if isinstance(error, commands.CommandOnCooldown):
			seconds = str(error).split()[-1]
			seconds = int(seconds[:-4])
			t = str(datetime.timedelta(seconds = seconds))
			h, m, s = t.split(':')
			await ctx.send(f'You are on cooldown. Try again in **{s}** seconds.')

	@daily.error
	async def daily_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			seconds = str(error).split()[-1]
			seconds = int(seconds[:-4])
			t = str(datetime.timedelta(seconds = seconds))
			h, m, s = t.split(':')

			embed = discord.Embed(color = 0xFF0000)
			embed.add_field(name = 'You already collected your daily', value = f'Next in **{h}:{m}:{s}**')

			await ctx.send(embed = embed)






def setup(client):
	client.add_cog(Gambling(client))