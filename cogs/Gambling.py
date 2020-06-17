import discord
import ezsheets
import random
import datetime
import time
import asyncio
from discord.ext import commands

"""
--------TO DO LIST-----------
DONE - Write the !bet command
DONE - Add in the !bet command error format
DONE - Come up with the !daily for credits
DONE - SlotMachine
DONE - !register command for new users, should make program run faster
DONE - Leaderboards
Create a shop system: Crates for xp and credits
Level system
DONE - !give a user
DONE - !gamble for help menu with gambling options

!horse or snail - out of 5, 5x payout

Done - !search command to find 25 - 100 coins on ground
Done - Stats with games played, overall profit and profit based on game
!lower command where you guess number lower than

"""

cooldowns = {}

STARTING_CREDITS = 5000
STARTING_CRATES = 0
STARTING_EXP = 0
STARTING_LEVEL = 1
DAILY_AMOUNT = 2500

BET_PAYOUT = 2



def level_checker(user):
	ss = ezsheets.Spreadsheet('14YXEduQ02xnWR7oB9tPpeCpoogPI-YwS9ycwNODxD68') #Opens up the google spreadsheets 'Tilted'
	sheet = ss['output']

	location = sheet.getColumn(1).index(user)
	location += 1

	name = str(sheet[3, location])

	gamesPlayed = int(sheet[10, location])
	if gamesPlayed % 30 == 0:
		print('Level up')
		level = int(gamesPlayed / 30)
		if level > 50:
			print('Max Level achieved')
			return False
		else:
			sheet[8, location] = level
			embed = discord.Embed(color = 0xAC6AFF, description = f'{name} has leveled up to Level {level}!')
			return embed

	else:
		return False




	response = str(number)
	return response

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
			credits = int(credits)
		#If the user doesn't exist yet
		else:
			await ctx.send('Please register first using `!register`.')
			return
		
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
				level = sheet[8, location]
				
				embed = discord.Embed(color = 3066993, title = f'User: {author.name} | Level: {level}')
				embed.add_field(name='Correct!', value = f'Number was **{dice}**', inline = True)
				embed.add_field(name='Profit', value = f'**{profit:,d}** credits', inline = True)
				embed.add_field(name='Credits', value = f'You have {credits:,d} credits', inline = False)

			else:
				profit = 0 - amount
				credits += profit
				sheet[5, location] = credits

				embed = discord.Embed(color = 0xFF0000, title = f'User: {author.name} | Level: {level}')
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

			response = level_checker(user)
			if response != False:
				await ctx.send(embed = response)





	@commands.command(aliases = ['slots', 'slotmachine'])
	@commands.cooldown(1, 7, commands.BucketType.user)
	async def slot(self, ctx, amount = None):

		ss = ezsheets.Spreadsheet('14YXEduQ02xnWR7oB9tPpeCpoogPI-YwS9ycwNODxD68') #Opens up the google spreadsheets 'Tilted'
		sheet = ss['output']



		slotIcons = [':medal:',':medal:',':medal:',':medal:',':medal:',':medal:',':medal:',':medal:',':medal:',':medal:',':medal:',':medal:',':medal:',':medal:',':medal:',':medal:',':medal:',':medal:',':medal:',':medal:',\
		':100:', ':100:',':100:', ':100:',':100:', ':100:',':100:', ':100:',':100:', ':100:',':100:', ':100:',':100:', ':100:',':100:', ':100:',':100:', ':100:',\
		':dollar:',':dollar:',':dollar:',':dollar:',':dollar:',':dollar:',':dollar:',':dollar:',':dollar:',':dollar:',':dollar:',':dollar:',':dollar:',':dollar:',\
		':moneybag:',':moneybag:',':moneybag:',':moneybag:',':moneybag:',':moneybag:',':moneybag:',':moneybag:',':moneybag:',':moneybag:',':moneybag:',':moneybag:',\
		':gem:',':gem:',':gem:',':gem:',':gem:',':gem:',':gem:']
		author = ctx.message.author
		user = author.id
		user = str(user)

		if user in sheet.getColumn(1):
			location = sheet.getColumn(1).index(user)
			location += 1
			credits = int(sheet[5, location])
			level = int(sheet[8, location])
		else:
			await ctx.send('Please register first using `!register`.')


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


		slot1 = random.randint(0,70)
		slot2 = random.randint(0,70)
		slot3 = random.randint(0,70)
		payout = 0

		embed = discord.Embed(color = 3066993)
		embed.add_field(name = f'Slot | User: {author.name} | Level: {level}', value = f'**---------------\n|<a:slot:722306708273234002>|<a:slot:722306708273234002>|<a:slot:722306708273234002>|\n---------------\n---SPINNING---**', inline = False)
		message = await ctx.send(embed = embed)
		time.sleep(.75)
		embed = discord.Embed(color = 3066993)
		embed.add_field(name = f'Slot | User: {author.name} | Level: {level}', value = f'**---------------\n|{slotIcons[slot1]}|<a:slot:722306708273234002>|<a:slot:722306708273234002>|\n---------------\n---SPINNING---**', inline = False)
		await message.edit(embed = embed)
		time.sleep(.75)
		embed = discord.Embed(color = 3066993)
		embed.add_field(name = f'Slot | User: {author.name} | Level: {level}', value = f'**---------------\n|{slotIcons[slot1]}|{slotIcons[slot2]}|<a:slot:722306708273234002>|\n---------------\n---SPINNING---**', inline = False)
		await message.edit(embed = embed)
		time.sleep(.75)
		embed = discord.Embed(color = 3066993)
		embed.add_field(name = f'Slot | User: {author.name} | Level: {level}', value = f'**---------------\n|{slotIcons[slot1]}|{slotIcons[slot2]}|{slotIcons[slot3]}|\n---------------\n---SPINNING---**', inline = False)
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
			result.add_field(name = f'Slot | User: {author.name} | Level: {level}', value = f'**---------------\n|{slotIcons[slot1]}|{slotIcons[slot2]}|{slotIcons[slot3]}|\n---------------\n---YOU WON---**', inline = False)
		else:
			result = discord.Embed(color = 0xFF0000)
			result.add_field(name = f'Slot | User: {author.name} | Level: {level}', value = f'**---------------\n|{slotIcons[slot1]}|{slotIcons[slot2]}|{slotIcons[slot3]}|\n---------------\n---YOU LOST---**', inline = False)

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

		response = level_checker(user)
		if response != False:
			await ctx.send(embed = response)


	@commands.command(aliases = ['horseduels'])
	@commands.cooldown(1, 10, commands.BucketType.user)
	async def horseduel(self, ctx, member : discord.Member = None, amount = None):
		ss = ezsheets.Spreadsheet('14YXEduQ02xnWR7oB9tPpeCpoogPI-YwS9ycwNODxD68') #Opens up the google spreadsheets 'Tilted'
		sheet = ss['output']

		global user
		user = member
		print(member)
		print(amount)

		def duel_acceptance(m):
			if m.author.id == member.id:
				if m.content.lower()[0] == 'y' or m.content.lower()[0] == 'n':
					return True
				else:
					return False
			else:
				return False	

		if member == None and amount == None:
			embed = discord.Embed(color = discord.Colour.orange())
			embed.add_field(name = 'Help', value = 'Race someone in a horse race', inline = False)
			embed.add_field(name = 'Payout', value ='Winner takes all', inline = False)
			embed.add_field(name = 'Usage', value = '**!horseduel @player <amount>**')
			await ctx.send(embed = embed)
			return

		elif member == None:
			embed = discord.Embed('Please @ a specific user')
			await ctx.send(embed = embed)
			return
		elif amount == None:
			embed = discord.Embed(description = 'Please enter a valid amount to bet')
			await ctx.send(embed = embed)
			return


		prompt = discord.Embed(color = 3066993, description = f'{member.name}, do you accept?\n**Yes** or **No**')
		await ctx.send(embed = prompt)

		try:
			msg = await self.client.wait_for('message', check=duel_acceptance, timeout=15)
		except Exception:
			return await ctx.send(f'Sorry, {member.name} took too long to answer. The race is off.')

		choice = msg.content[0]
		if choice.lower() != 'y' and choice.lower() != 'n':
			await ctx.send('Invalid acceptance. Next time use `yes` or `no`.')
			return
		elif choice.lower() == 'n':
			amount = int(amount)
			await ctx.send(f'{member.name} has declined the horse race for {amount:,d} credits.')
			return


		amount = int(amount)
		user = member.id
		user = str(user)

		author = ctx.message.author
		author = author.id
		author = str(author)

		if author in sheet.getColumn(1):
			location = sheet.getColumn(1).index(author)
			location += 1
			authorCredits = sheet[5, location]
			authorCredits = int(authorCredits)
		else:
			await ctx.send(f'You have yet to register with `!register`.')
			return

		if user in sheet.getColumn(1):
			ULocation = sheet.getColumn(1).index(user)
			ULocation += 1
			UCredits = sheet[5, ULocation]
			UCredits = int(UCredits) 
		else:
			await ctx.send(f'{member.mention} has yet to register with `!register`.')
			return

		if int(amount) > authorCredits:
			await ctx.send(f'{ctx.message.author.mention}, you do not have sufficient credits.')
			return
		if int(amount) > UCredits:
			await ctx.send(f'{member.mention}, you do not have sufficient credits')
			return


		horse = '🏇'
		flag = ':checkered_flag:'
		horse_track1 = ' - - - - - - - - - - '
		horse_track2 = ' - - - - - - - - - - '

		horse = discord.Embed(color = 3066993)
		horse.add_field(name = f'Horse Duel | {ctx.message.author.name} vs. {member.name}', value = f'{flag}{horse_track1}🏇 **{ctx.message.author.name}**\n{flag}{horse_track2}🏇 **{member.name}**')

		race = 	await ctx.send(embed = horse)

		while horse_track1 != '' and horse_track2 != '':
			time.sleep(1.5)
			horse1 = random.randint(0,2) * 2
			horse2 = random.randint(0,2) * 2

			if horse1 != 0:
				horse_track1 = horse_track1[:-horse1]
			if horse2 != 0:
				horse_track2 = horse_track2[:-horse2]
			embed = discord.Embed(color = 3066993)
			embed.add_field(name = f'Horse Duel | {ctx.message.author.name} vs. {member.name}', value = f'{flag}{horse_track1}🏇 **{ctx.message.author.name}**\n{flag}{horse_track2}🏇 **{member.name}**')
			await race.edit(embed = embed)

		if horse_track1 == '' and horse_track2 == '':
			winner = None
			embed.add_field(name = '-------------------------------', value = f'It was a Tie!', inline = False)
			embed.add_field(name = 'Profit', value = f'**0** credits', inline = False)
			race.edit(embed = embed)


		elif horse_track1 == '':
			winner = ctx.message.author.mention
			authorCredits += amount
			UCredits -= amount
			sheet[5, location] = authorCredits
			sheet[5, ULocation] = UCredits
		else:
			winner = member.mention
			authorCredits -= amount
			UCredits += amount
			sheet[5, location] = authorCredits
			sheet[5, ULocation] = UCredits


		embed.add_field(name = '-------------------------------', value = f'{winner} Won!', inline = False)
		embed.add_field(name = 'Profit', value = f'**{amount}** credits', inline = False)

		await race.edit(embed = embed)


		#MISSING GAMES PLAYED


		response = level_checker(author)
		if response != False:
			await ctx.send(embed = response)

		response = level_checker(user)
		if response != False:
			await ctx.send(embed = response)



	"""
	@commands.command(aliases = ['cooldowns'])
	async def cooldown(self, ctx):
		global cooldowns

		print(cooldowns)

		#Time to be completed
		timer = cooldowns[str(ctx.author.id)] #This is the future time, the 24 hours

		print(timer)
		print(datetime.datetime.now())

		timer = timer - datetime.datetime.now() 

		print(timer)
		print(str(timer))

		if str(timer)[0] == '-': #Finds if the cooldown has already been completed
			timer = 'Done'




		print(f'Your cooldown is {timer}')

"""






	@commands.command(aliases = ['registers', 'signup'])
	async def register(self, ctx):
		author = ctx.message.author
		user = author.id
		user = str(user)


		ss = ezsheets.Spreadsheet('14YXEduQ02xnWR7oB9tPpeCpoogPI-YwS9ycwNODxD68') #Opens up the google spreadsheets 'Tilted'
		sheet = ss['output']


		#If the user exists
		if user in sheet.getColumn(1):
			await ctx.send('You have already been registered.')
		#If the user doesn't exist yet
		else:
			empty = sheet.getColumn(1).index('')
			location = empty + 1
			sheet[1, location] = user
			sheet[3, location] = author.name
			sheet[5, location] = STARTING_CREDITS
			sheet[6, location] = STARTING_CRATES
			sheet[7, location] = STARTING_EXP
			sheet[8, location] = STARTING_LEVEL
			sheet[9, location] = 0
			sheet[10, location] = 0
			sheet[11, location] = 0
			sheet[12, location] = 0
			await ctx.send('You have successfully been registered!')

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
			credits = int(credits)
		#If the user doesn't exist yet
		else:
			await ctx.send('Please register first using `!register`.')

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
			credits = int(credits)
		#If the user doesn't exist yet
		else:
			await ctx.send('Please register first using `!register`.')

		credits += DAILY_AMOUNT
		sheet[5,location] = credits

		embed = discord.Embed(color = 3066993)
		embed.add_field(name = f'You got {DAILY_AMOUNT:,d} credits', value = f'You have {credits:,d} credits', inline = False)

		"""
		#Cooldown function for viewing cooldowns

		global cooldowns
		now = datetime.datetime.now()#This is the current time
		future = now + datetime.timedelta(seconds=30)#Add 24 hours to the time, getting time next value can be completed

		cooldowns[str(ctx.author.id)] = future
		"""
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
			credits = int(credits)
		#If the user doesn't exist yet
		else:
			await ctx.send('Please register first using `!register`.')

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

	@commands.command()
	async def give(self, ctx, member : discord.Member = None, amount = None):
		ss = ezsheets.Spreadsheet('14YXEduQ02xnWR7oB9tPpeCpoogPI-YwS9ycwNODxD68') #Opens up the google spreadsheets 'Tilted'
		sheet = ss['output']

		if member == None and amount == None:
			embed = discord.Embed(color = 0x607d8b)
			embed.add_field(name = 'Help', value = 'Give a player some of your credits', inline = False)
			embed.add_field(name = 'Usage', value = '**!give @player <amount>**')

		elif member == None or member.isdigit():
			embed = discord.Embed('Please @ a specific user')
			await ctx.send(embed = embed)
			return
		elif amount == None:
			embed = discord.Embed(description = 'Please enter a valid amount to give')
			await ctx.send(embed = embed)
			return


		amount = int(amount)
		user = member.id
		user = str(user)

		author = ctx.message.author
		author = author.id
		author = str(author)

		if author in sheet.getColumn(1):
			location = sheet.getColumn(1).index(author)
			location += 1
			authorCredits = sheet[5, location]
			authorCredits = int(authorCredits)
		else:
			await ctx.send(f'You have yet to register with `!register`.')
			return

		if user in sheet.getColumn(1):
			ULocation = sheet.getColumn(1).index(user)
			ULocation += 1
			UCredits = sheet[5, ULocation]
			UCredits = int(UCredits) 
		else:
			await ctx.send(f'{member.mention} has yet to register with `!register`.')
			return

		if int(amount) > authorCredits:
			await ctx.send(f'You do not have that amount to give.')
			return

		UCredits += amount
		authorCredits -= amount
		sheet[5, ULocation] = UCredits
		sheet[5, location] = authorCredits


		embed = discord.Embed(description = f'You gave {member.mention} {amount:,d} credits.')

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
			credits = int(credits)
		#If the user doesn't exist yet
		else:
			await ctx.send('Please register first using `!register`.')

		totalProf = int(sheet[9, location])
		gamesPlayed = int(sheet[10, location])
		level = int(sheet[8, location])
		betProfit = int(sheet[11, location])
		slotProfit = int(sheet[12, location]) 

		embed = discord.Embed(color = 0xffff00, title = f'Stats for: {author.name}')
		embed.add_field(name = 'Total Profit', value = f'{totalProf:,d}', inline = True)
		embed.add_field(name = 'Games Played', value = f'{gamesPlayed}', inline = True)
		embed.add_field(name = 'Level', value =f'{level}', inline = True)
		embed.add_field(name = 'High Low Profit', value = f'{betProfit:,d}', inline = True)
		embed.add_field(name = 'Slots Profit', value = f'{slotProfit:,d}', inline = True)
		embed.set_footer(text = f'You currently have {credits:,d} credits.')

		await ctx.send(embed = embed)

	@commands.command(aliases =['gambling', 'gambler'])
	async def gamble(self, ctx):

	#Sends these privately to the user
	#author = ctx.message.author
	#await author.send(embed = embed)

		embed = discord.Embed(
		colour = discord.Colour.orange(),
		title = 'Gambling Help',
		description = 'Get the highest credit amount in the server or buy some cool items from the shop!'
		)

		fields = [(':game_die: Games :game_die:', '`!bet`, `!slots`, `!horseduel`', False),
			  (':gear: Other :gear:', '`!register`, `!credits`, `!daily`, `!search`, `!give`, `!leaderboard`, `!loserboard`, `!stats`', False)]

		for name, value, inline in fields:
			embed.add_field(name=name, value=value, inline = inline)


		await ctx.send(embed = embed)

	@commands.command(aliases =['names', 'change'])
	async def name(self, ctx, new = None):
		ss = ezsheets.Spreadsheet('14YXEduQ02xnWR7oB9tPpeCpoogPI-YwS9ycwNODxD68') #Opens up the google spreadsheets 'Tilted'
		sheet = ss['output']

		if new == None: #Help men
			embed = discord.Embed(color = discord.Colour.orange())
			embed.add_field(name = 'Help', value = 'Changes the name that the bot calls you.', inline = False)
			embed.add_field(name = 'Usage', value = '**!name <name>**', inline = False)

		else:
			if str(ctx.author.id) in sheet.getColumn(1):
				location = sheet.getColumn(1).index(str(ctx.author.id))
				location += 1
				credits = sheet[5, location]
				credits = int(credits)
			#If the user doesn't exist yet
			else:
				await ctx.send('Please register first using `!register`.')
				return

			sheet[3, location] = new
			embed = discord.Embed(color = discord.Colour.orange(), description = f'Your name has been changed in the bots records to {new}.')
			
		
		await ctx.send(embed = embed)













	#ERROR HANDLING
	@bet.error
	async def bet_error(self, ctx, error):
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

	@slot.error
	async def slot_error(self, ctx, error):
		if isinstance(error, commands.CommandOnCooldown):
			seconds = str(error).split()[-1]
			seconds = int(seconds[:-4])
			t = str(datetime.timedelta(seconds = seconds))
			h, m, s = t.split(':')

			embed = discord.Embed(color = 0xFF0000)
			embed.add_field(name = 'You are going to fast.', value = f'Next in **{h}:{m}:{s}**')

			await ctx.send(embed = embed)






def setup(client):
	client.add_cog(Gambling(client))