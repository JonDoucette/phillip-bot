import discord
import ezsheets
import random
import datetime
import time
from discord.ext import commands

"""
--------TO DO LIST-----------
DONE - Write the !bet command
DONE - Add in the !bet command error format
DONE - Come up with the !daily for credits

Done - SlotMachine

!register command for new users, should make program run faster

DONE - Leaderboards
Create a shop system: Crates for xp and credits
Level system
!lower command where you guess number lower than

Done - !search command to find 25 - 100 coins on ground
Done - Stats with games played, overall profit and profit based on game

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

	@commands.command(aliases = ['slots', 'slotmachine'])
	async def slot(self, ctx, amount = None):

		ss = ezsheets.Spreadsheet('14YXEduQ02xnWR7oB9tPpeCpoogPI-YwS9ycwNODxD68') #Opens up the google spreadsheets 'Tilted'
		sheet = ss['output']



		slotIcons = [':medal:',':medal:',':100:', ':100:', ':dollar:',':dollar:', ':moneybag:',':moneybag:', ':gem:']
		author = ctx.message.author
		user = author.id
		user = str(user)

		location = sheet.getColumn(1).index(user)
		location += 1
		credits = int(sheet[5, location])


		if amount == None:
			embed = discord.Embed(color = discord.Colour.orange())
			embed.add_field(name = 'Help', value = 'Slot machine', inline = False)
			embed.add_field(name = 'Winnings', value = ':medal::medal::grey_question: - **0.5x**\n\
														:100::100::grey_question: - **2x**\n\
														:dollar::dollar::grey_question: - **2x**\n\
														:medal::medal::medal: - **2.5x**\n\
														:100::100::100: - **3x**\n\
														:moneybag::moneybag::grey_question: - **3.5x**\n\
														:dollar::dollar::dollar: - **4x**\n\
														:gem::gem::grey_question: - **7x**\n\
														:moneybag::moneybag::moneybag: - **7x**\n\
														:gem::gem::gem: - **15x**', inline = False)
			embed.add_field(name = 'Usage', value = '**!slots <amount>**')
			await ctx.send(embed = embed)
			return
		elif not amount.isdigit():
			await ctx.send('Please enter a digit amount for your bet.')
			return 
		elif int(amount) > credits:
			await ctx.send('You do not have enough credits.')
			return


		slot1 = random.randint(0,8)
		slot2 = random.randint(0,8)
		slot3 = random.randint(0,8)
		payout = 0

		embed = discord.Embed(color = 3066993)
		embed.add_field(name = f'Slot | User: {author.name}', value = f'**---------------\n|<a:slot:722306708273234002>|<a:slot:722306708273234002>|<a:slot:722306708273234002>|\n---------------\n---SPINNING---**', inline = False)
		message = await ctx.send(embed = embed)
		time.sleep(.75)
		embed = discord.Embed(color = 3066993)
		embed.add_field(name = f'Slot | User: {author.name}', value = f'**---------------\n|{slotIcons[slot1]}|<a:slot:722306708273234002>|<a:slot:722306708273234002>|\n---------------\n---SPINNING---**', inline = False)
		await message.edit(embed = embed)
		time.sleep(.75)
		embed = discord.Embed(color = 3066993)
		embed.add_field(name = f'Slot | User: {author.name}', value = f'**---------------\n|{slotIcons[slot1]}|{slotIcons[slot2]}|<a:slot:722306708273234002>|\n---------------\n---SPINNING---**', inline = False)
		await message.edit(embed = embed)
		time.sleep(.75)
		embed = discord.Embed(color = 3066993)
		embed.add_field(name = f'Slot | User: {author.name}', value = f'**---------------\n|{slotIcons[slot1]}|{slotIcons[slot2]}|{slotIcons[slot3]}|\n---------------\n---SPINNING---**', inline = False)
		await message.edit(embed = embed)




		if slotIcons[slot1] != slotIcons[slot2] and slotIcons[slot2] != slotIcons[slot3]:
			payout = -1
		elif slotIcons[slot1] == slotIcons[slot2] and slotIcons[slot1] == slotIcons[slot3]:
			if slotIcons[slot1] == ':medal:':
				medalWin = int(sheet[15, 2])
				medalWin += 1
				sheet[15,2] = medalWin
				payout = 2.5
			elif slotIcons[slot1] == ':100:':
				medalWin = int(sheet[16, 2])
				medalWin += 1
				sheet[16,2] = medalWin
				payout = 3
			elif slotIcons[slot1] == ':dollar:':
				medalWin = int(sheet[17, 2])
				medalWin += 1
				sheet[17,2] = medalWin
				payout = 4
			elif slotIcons[slot1] == ':moneybag:':
				medalWin = int(sheet[18, 2])
				medalWin += 1
				sheet[18,2] = medalWin
				payout = 7
			elif slotIcons[slot1] == ':gem:':
				medalWin = int(sheet[19, 2])
				medalWin += 1
				sheet[19,2] = medalWin
				payout = 15
		elif slotIcons[slot1] == slotIcons[slot2] and slotIcons[slot1] != slotIcons[slot3]:
			if slotIcons[slot1] == ':medal:':
				Win = int(sheet[15, 2])
				Win += 1
				sheet[15,2] = Win
				payout = 0.5
			elif slotIcons[slot1] == ':100:':
				Win = int(sheet[16, 2])
				Win += 1
				sheet[16,2] = Win
				payout = 2
			elif slotIcons[slot1] == ':dollar:':
				Win = int(sheet[17, 2])
				Win += 1
				sheet[17,2] = Win
				payout = 2
			elif slotIcons[slot1] == ':moneybag:':
				Win = int(sheet[18, 2])
				Win += 1
				sheet[18,2] = Win
				payout = 3.5
			elif slotIcons[slot1] == ':gem:':
				Win = int(sheet[19, 2])
				Win += 1
				sheet[19,2] = Win
				payout = 7
		elif slotIcons[slot1] != slotIcons[slot2] and slotIcons[slot2] == slotIcons[slot3]:
			if slotIcons[slot2] == ':medal:':
				Win = int(sheet[15, 2])
				Win += 1
				sheet[15,2] = Win
				payout = 0.5
			elif slotIcons[slot2] == ':100:':
				Win = int(sheet[16, 2])
				Win += 1
				sheet[16,2] = Win
				payout = 2
			elif slotIcons[slot2] == ':dollar:':
				Win = int(sheet[17, 2])
				Win += 1
				sheet[17,2] = Win
				payout = 2
			elif slotIcons[slot2] == ':moneybag:':
				Win = int(sheet[18, 2])
				Win += 1
				sheet[18,2] = Win
				payout = 3.5
			elif slotIcons[slot2] == ':gem:':
				Win = int(sheet[19, 2])
				Win += 1
				sheet[19,2] = Win
				payout = 7

		amount = int(amount)
		location = sheet.getColumn(1).index(user)
		location += 1
		credits = int(sheet[5, location])

		profit = int(amount*payout)
		credits = int(credits + profit)
		sheet[5, location] = credits

		if payout != -1:
			result = discord.Embed(color = 3066993)
			result.add_field(name = f'Slot | User: {author.name}', value = f'**---------------\n|{slotIcons[slot1]}|{slotIcons[slot2]}|{slotIcons[slot3]}|\n---------------\n---YOU WON---**', inline = False)
		else:
			result = discord.Embed(color = 0xFF0000)
			result.add_field(name = f'Slot | User: {author.name}', value = f'**---------------\n|{slotIcons[slot1]}|{slotIcons[slot2]}|{slotIcons[slot3]}|\n---------------\n---YOU LOST---**', inline = False)

		result.add_field(name = 'Profit', value = f'**{profit:,.0f}** credits', inline = True)
		result.add_field(name = 'Credits', value = f'You have {credits:,.0f} credits', inline = True)

		await message.edit(embed = result)

		#Adds data to the statistics
		totalProf = int(sheet[9, location])
		totalProf += profit
		sheet[9, location] = totalProf

		gamesPlayed = int(sheet[10, location])
		gamesPlayed += 1
		sheet[10, location] = gamesPlayed

		slotProfit = int(sheet[12, location])
		slotProfit += profit
		sheet[12, location] = slotProfit

		#For balancing purposes in the future
		slotsPlayed = int(sheet[13, 2])
		slotsPlayed += 1
		sheet[13, 2] = slotsPlayed

		if payout != -1:
			slotsWon = int(sheet[14, 2])
			slotsWon += 1
			sheet[14, 2] = slotsWon

	@commands.command(aliases = ['credit', 'balance'])
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
		slotProfit = int(sheet[12, location]) 

		embed = discord.Embed(color = 0xffff00, title = f'Stats for: {author.name}')
		embed.add_field(name = 'Total Profit', value = f'{totalProf:,d}', inline = True)
		embed.add_field(name = 'Games Played', value = f'{gamesPlayed}', inline = True)
		embed.add_field(name = 'High Low Profit', value = f'{betProfit:,d}', inline = True)
		embed.add_field(name = 'Slots Profit', value = f'{slotProfit:,d}', inline = True)
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