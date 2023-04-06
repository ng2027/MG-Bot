import discord, re, enchant
from discord.ext import commands, tasks
from math import floor
from time import sleep
from discord import Embed
from PyDictionary import PyDictionary
value = 0
numbers = '1234567890'
consants = 'bcdfghjklmnpqrstvwxyz'
master_list = 'abcdefghijklmnopqrstuvwxyz1234567890._'
period = '.'
underscore = '_'
vowel = 'aeiou'
un = ''
og_value = 0
alphabets = 'abcdefghijklmopqrstuvwxyz'
check_word_is_real_word = enchant.Dict("en_US")

"""
Value Cog
    value command- 1,2,3,4 letter username approximate values. Incase of price change, VALUE MUST BE MANUALLY CHANGED
    Return value of username
    ogvalue command- Checks if username is appraised. If no checks if it is an actual word.
    Return value of OG username
    appraise command- Appraise a user,
"""
class Value(commands.Cog):

    def __init__(self, client):
        self.client = client

    #Username Class, stores each seperate character value 
    class Username:
        #values to add if character is......
        def __init__(self, length, value, consants, vowel, period, underscore, number):
            self.length = length
            self.value = value
            self.consants = consants
            self.vowel = vowel
            self.period = period
            self.underscore = underscore
            self.number = number
    #Repeater Class, Incase of repeater, Checks how much letter repeated and assigns value           
    class repeater:
        def __init__(self, length, repeat_1, repeat_2, repeat_3): #n**l #n***  #**** /// #n**  #*** /// #**
            self.length = length                                        #repeat_1 - 2characters repeated
            self.repeat_1 = repeat_1                                    #repeat_2 - 3 characters repeated/ +*+*
            self.repeat_2 = repeat_2                                    #repeat_3 - 4 characters repeated
            self.repeat_3 = repeat_3
            
    #Starting base price, given by sorting characters
    def intial_check(letters, length):
        global new_value
        if letters in numbers:
            new_value = new_value + Value.base_value[length-2].number
        elif letters in consants:
            new_value = new_value + Value.base_value[length-2].consants
        elif letters in period:
            new_value = new_value + Value.base_value[length-2].period
        elif letters in underscore:
            new_value = new_value + Value.base_value[length-2].underscore
        elif letters in vowel:
            new_value = new_value + Value.base_value[length-2].vowel
    #assigns value according to repeater      
    def repeater_check(repeaters_found, length):
        global new_value
        if repeaters_found == 1:
            new_value = new_value + Value.repeat_values[length-2].repeat_1
        elif repeaters_found == 2:
            new_value = new_value + Value.repeat_values[length-2].repeat_2
        elif repeaters_found ==3:
            new_value = new_value + Value.repeat_values[length-2].repeat_3
     #check if username is pronounceable       
    def pronounceable_check(username, length):
        global new_value
        if length == 4 and username[1] in vowel and username[3] in vowel:
            new_value = new_value + 20  ########################################## VALUE CHANGEABLE #################
        elif length == 3 and username[1] in vowel:
            new_value = new_value + 95 ########################################## VALUE CHANGEABLE #################
            
     #checks if all number       
    def allnumber_check(username):
        global new_value
        try:
            checking__ = int(username)
            new_value = round(new_value*3.8) ########################################## VALUE CHANGEABLE #################
        except:
            new_value = new_value
     #check all underscore       
    def check_allunderscore(username, length):
        global un, new_value
        for i in range(length):
            un += '_'
        if un == username:
            new_value = new_value*5
            
    def impossible_username_check(username, length):
        global new_value
        if username[0] == '.' or username[length-1] == '.':
            new_value = 0
    def illegal_character_check(username):
        global new_value
        rex = re.compile('[!@#$%^&*()-+={}\|":;<>,?/]')
        search = rex.search(username)
        if search == None:
            new_value = new_value
        else:
            new_value = 0
     ########################################## VALUE CHANGEABLE ########################################
            
    base_value = [ Username(2, 5000, 400, 600, 1200, 1000, -800),   #2letter   REFERENCE TO Username CLASS
                   Username(3,500, 15, 30, 120, 100, -50 ),         #3letter   REFERENCE TO Username CLASS
                   Username(4, 33, 1, 4, 20, 15, -5),               #4letter   REFERENCE TO Username CLASS
                   Username(1, 25000, 0, 3000, 0, 0, 0)]            #1letter   REFERENCE TO Username CLASS

    ########################################## VALUE CHANGEABLE ######################################
    
    repeat_values = [ repeater(2,9000 ,0 , 0 ),         #2letter REFERENCE TO repeater CLASS
                repeater(3,700 ,4000 ,0 ),              #3letter REFERENCE TO repeater CLASS
                repeater(4,20 ,160 ,2300  ),            #4letter REFERENCE TO repeater CLASS
                repeater(1,0 ,0 ,0 )]                   #1letter REFERENCE TO repeater CLASS

    #Value Command
    @commands.command(
        pass_context = True,
        description = 'This command estimates the price of a username. It is not 100% accurate.'
        )
    async def value(self, ctx, username):
        try:
            global new_value
            username = username.lower()

            #unecessary easter egg
            if username == 'maij':
                embed = Embed(color = 16711680)
                embed.add_field(name="mj", value="BOSS MAN", inline=True)
                await ctx.send(embed=embed)
            elif username == 'n0e1':
                embed = Embed(color = 16711680)
                embed.add_field(name="ng", value="O_O", inline=True)
                await ctx.send(embed=embed)
            else:
                username_recheck_repeat = []
                repeaters_found = 0
                length = len(username)
                if length < 5: #checks if user under 5 characters               
                    intial_value = Value.base_value[length-2].value   #assigns a base value to add/subtract new valye BASE VALUE
                    new_value = intial_value
                    for letters in username:                            #Repeater find
                        Value.intial_check(letters, length)             #
                        if letters in username_recheck_repeat:          #If repeater found, increases the repeater_found +1
                            repeaters_found += 1                        #
                            username_recheck_repeat.remove(letters)     #
                        username_recheck_repeat += letters
                        
                    if repeaters_found >0:
                        Value.repeater_check(repeaters_found, length)
                    else:
                        new_value = new_value
                    Value.pronounceable_check(username, length)
                    Value.allnumber_check(username)
                    Value.check_allunderscore(username, length)
                    Value.impossible_username_check(username, length)
                    Value.illegal_character_check(username)
                    embed = Embed(color = 16711680)
                    embed.add_field(name="Estimated value:", value=f'{new_value}$')
                    await ctx.send(embed=embed)
                else:
                    check_og_ = check_word_is_real_word.check(username.upper())
                    if check_og_ == True:
                        embed = Embed(color = 16711680)
                        embed.add_field(name="OG Detected *ERROR*", value="This command works for 4 letter users and below.\nTry **!help ogvalue** to get the value of the OG usernames.")
                        await ctx.send(embed=embed)
                    else:
                        embed = Embed(color = 16711680)
                        embed.add_field(name = '404', value = 'random user')
                        await ctx.send(embed=embed)
        except Exception as error101:
            print(error101)
            await ctx.send('There has been an error using the !value command')

    ###################################
                    #OGVALUE
    class OGUsername:
        def __init__(self, length, value):
            self.length = length
            self.value = value
     #assigns base value, if not appraiseds       
    og_base_value = [OGUsername(1, 25000), OGUsername(2, 5000),
                     OGUsername(3, 550), OGUsername(4, 150), OGUsername(5, 90)] ##########VALUE CHANGE######

    def semi_check(username):
        global new_value, length
        if username[-1] == 's':
            new_value = round(Value.og_base_value[length - 2].value / 1.9)
    @commands.command(
        pass_context = True,
        description = 'This command estimates the value of an OG username. Example: !ogvalue sword. It is not 100% accurate.'
        )
    async def ogvalue(self, ctx, username):
        try:
            global new_value, length
            username = username.lower()
            check_og = check_word_is_real_word.check(username.upper())  #USES PYENCHANT module to check if word is a real word
            length = len(username)
            first_letter = username[0]
            file_og = open(first_letter + 'price.txt', 'r')  #Due to use of txt, file ORGANISES into Seperate Files According to first letter
            user_present = False

            #checks if user is appraised
            for line in file_og:
                if username in line:
                    user_name_in = line.split('\n')[0].split(':')[0]
                    if username == user_name_in:
                        user_present = True
                        username = line  #if user present line == username

            if user_present == True:
                value = username.split('\n')[0].split(':')[1]
                embed = Embed(color = 16711680)
                embed.add_field(name="Appraised OG price:", value=f'{str(value)}$')
                await ctx.send(embed=embed)
             #if user is not appraised estimated price NOTE NOT ACCURATE AT ALL   
            else:
                if check_og == True:
                    if len(username) < 6:
                        new_value = Value.og_base_value[length - 1].value
                        Value.semi_check(username)
                        embed = Embed(color = 16711680)
                        embed.add_field(name="Estimated OG price:", value=f'{str(new_value)}$')
                        await ctx.send(embed=embed)
                    else:
                        embed = Embed(color = 16711680)
                        embed.add_field(name="An error has been spotted.",
                                        value="The username is an OG but is over 5 letters long so I am unable to estimate its value. Give it a price using the !appraise command.")
                        await ctx.send(embed=embed)
                else:
                    embed = Embed(color = 16711680)
                    embed.add_field(name="Hmm. I am a robot.", value="This username is not an OG.'")
                    embed.set_image(url = 'https://media1.tenor.com/images/a936ff29339ce82004ad5a2dbe047362/tenor.gif?itemid=9754428')
                    await ctx.send(embed=embed)
        except Exception as error101:
            print(error101)
            await ctx.send('There has been an error using the !ogvalue command')
       #############################
                #appraise command
    def check_username_existed(username, lst):
        for element in lst:
            if username in element:
                user_appraised_ = element.split('\n')[0].split(':')[0]
                if username == user_appraised_:
                    return True
        return False

    @commands.command(
        pass_context = True,
        description = 'This command allows you to give your price for a username. Example: !appraise sword 1000'
        )
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def appraise(self, ctx, username, value):
        try:
            username = username.lower()
            user_letter = username[0]
            #if user contains number or special character cant appraise
            if username.isalpha():
                file_og = open(user_letter + 'price.txt', 'r')
                listfile_og = file_og.readlines()
                file_og.close()
                file_og = open(user_letter + 'price.txt', 'w')
                listfile_og.append("")
                iterations = 1
                times_to_loop = len(listfile_og)
                for element in listfile_og:                                                 #checks if user present in appraisal
                    iterations += 1                                                         #if present finds previous appraised price then finds the average
                    if iterations > times_to_loop: break                                    #new appraised value == AVERAGE VALUE
                    step1 = element.split("\n")[0].split(":")                               #if user not present writes the appraisal into txt
                    step2 = (float(step1[1]) + float(value)) / 2
                    if not Value.check_username_existed(username, listfile_og):
                        file_og.write(f"{username}:{value}\n")

                    if username != step1[0]:
                        file_og.write(f"{step1[0]}:{step1[1]}\n")
                    else:
                        file_og.write(f"{username}:{floor(step2)}\n")


                file_og.close()
                embed = Embed(color = 16711680)
                embed.add_field(name="Appraisal completed.", value="✅ appraised")
                await ctx.send(embed=embed)
            else:
                await ctx.send("``Beep Boop``")
                embed = Embed(color = 16711680)
                sleep(1.5)
                embed.add_field(name="BROKEN", value="The username you are trying to appraise is not an OG since it contains special characters/ numbers.")
                await ctx.send(embed=embed)
        except Exception as error101:
            print(error101)
            await ctx.send('There has been as error using the !appraise command')


     #meaning command       
    @commands.command(
        pass_context = True,
        description = 'This command returns the meaning of a word. You can use this to check if a username is in the dictionary. Example: !meaning sword'
        )
    async def meaning(self, ctx, username):
        try:
            member = ctx.message.author.name
            username = username.lower()
            check_og = check_word_is_real_word.check(username.upper())
            if check_og == True:
                if len(username) != 1:
                    dictionary=PyDictionary()
                    embed = Embed(color = 16711680)
                    embed.set_author(name=f'Meaning of {username}: ')
                    meaning_user = dictionary.meaning(username)
                    if meaning_user != None:
                        type_of_user = str(meaning_user).split(':')[0].replace("'",'').replace('{','')
                        define = meaning_user.values()
                        value_iterator = iter(define)                                                               #If username is og, checks for meaning
                        meaning = next(value_iterator)[0]                                                           #If meaning present, collects word type, and first meaning
                        embed.add_field(name = type_of_user, value = meaning)
                        await ctx.send(embed = embed)
                
            else:
                embed = Embed(color = 16711680)
                embed.add_field(name = f'{member} really created a new language', value = ':egg: ')
                await ctx.send(embed = embed)
        except Exception as error101:
            print(error101)
            await ctx.send('There has been as error using the !meaning command')
        
def setup(client):
    client.add_cog(Value(client))
    
