import sqlite3, discord, re, random, asyncio
from io import BytesIO

import certifi
import pycurl
from time import sleep
from discord.ext import commands
from dhooks import Embed
from random import choice
from random import randint
import requests
import traceback
import datetime

"""
MARKET COG-

SQL TABLE STRUCTURE,
SELL, SOLD, OFFER, BUY, BUDGET, BIN, CO
"""
#######################################################################TABLE STRUCTURE###########################################
# cmj.execute(""" CREATE TABLE mjmarket(
# listing_number INTEGER  PRIMARY KEY,
# username TEXT(30) NOT NULL UNIQUE,
# binprice INTEGER NOT NULL,
# seller_name TEXT(35) NOT NULL,
# current_offer INTEGER DEFAULT 0,
# highest_bidder TEXT(35) DEFAULT 0,
# note TEXT(100),
# prev_co INTEGER DEFAULT 0,
# prev_bidder TEXT DEFAULT 0
# )""")
# cmj.execute("CREATE TABLE boosters("
#             "checker_id INTEGER DEFAULT 0, "
#             "username TEXT(30)"
#             ")")

# cmj.execute("""CREATE TABLE budget_people(
# user_id TEXT(35) NOT NULL PRIMARY KEY,
# budget INTEGER DEFAULT 0"""
# )


#
# cmj.execute("CREATE TABLE ban_info_mod("
#             "mod_id TEXT(35) PRIMARY KEY,"
#             "last_ban TEXT(12)"
#             ")")
# cmj.execute("CREATE TABLE warnings_mod("
#             "mod_id TEXT(35) ,"
#             "warned_member_id TEXT(35),"
#             "warning_ID INT AUTO_INCREMENT"
#             ")")
# CREATE TABLE socialmedia(
# member_id TEXT (35) PRIMARY KEY,
# discord_user TEXT(35) DEFAULT 'Has not been set',
# instagram TEXT(30) DEFAULT 'Has not been set',
# telegram TEXT(32) DEFAULT 'Has not been set',
# ogu TEXT(40) DEFAULT 'Has not been set',
# kik TEXT (40) DEFAULT 'Has not been set',
# tiktok TEXT (40) DEFAULT 'Has not been set'
# );

# mj_market db access
# cmj cursor for mj_market

sentences = [
"MG BOT> EBAY",
"beep boop",
"-- --. / -... --- -"
]


async def _sell(self, ctx, username, bin_price, *note):
    mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
    cmj = mj_market.cursor()
    try:
        global claimed

        # used to stop error from guild.message used later in code LINE NO: 108+ Only for sell command
        if "Direct" in str(ctx.channel):
            embed = Embed(color = 16711680)
            embed.add_field(name="Please use this command in MJ's server. This command cannot be used in private.",
                            value=":poop: <','> :nerd:")
            await ctx.send(embed=embed)
            return
        # check if bin price is an number
        try:
            if '$' in bin_price:
                bin_price = bin_price.replace('$', '')
            check_number_bin = int(bin_price)
        except:
            embed = Embed(color = 16711680)
            embed.add_field(name='x æ a-12', value='BIN price is not a number.')
            await ctx.send(embed=embed)
            return
        # note required

        note = str(note).replace("'", "").replace(",", "").replace("(", "").replace(")", "")
        if len(note) == 0:
            embed = Embed(color = 16711680)
            embed.add_field(name="Please add a note!",
                            value="Please add a note to the buyers. !sell maij 50 comes with oge, pp and btc accepted.")
            await ctx.send(embed=embed)
            return

        # checks for illegal character
        if '@' in username[0]:
            username = username.replace('@', '')
        illegalcharacter = re.compile('[!@#$%^&*()-+={}|\":;<>,?/]')
        search = illegalcharacter.search(username)
        if search != None:
            embed = Embed(color = 16711680)
            embed.add_field(name='(☉ ౪ ⊙)',
                            value='please remove illegal characters from the username and try again! that includes the @ sign.')
            await ctx.send(embed=embed)
            return

        username = username.lower()
        seller_name = ctx.message.author.id
        try:
            cmj.execute(
                "INSERT INTO mjmarket(username, binprice, seller_name, note) VALUES(:username, :binprice, :seller_name, :note)",
                {'username': username, 'binprice': int(bin_price), 'seller_name': str(seller_name), "note": note})
            mj_market.commit()
        except Exception as error101:
            # too make sure the same user cant be sold twice
            if str(error101) == 'UNIQUE constraint failed: mjmarket.username':
                embed = Embed(color = 16711680)
                embed.add_field(name="Scammer?",
                                value="hmmm.... :liar:\nIt looks like there was a problem confirming you own this "
                                      "account. Make sure to remove any $ signs or @ signs. If you do own it, please provide proof you own the account to the admins.")
                await ctx.send(embed=embed)
            else:
                print(error101)
                await ctx.send('There has been an error using !sell command')
            return
        await ctx.message.add_reaction('✅')

        roles = ctx.author.roles  # get users role, checks for top role
        role1 = discord.utils.get(ctx.guild.roles,
                                  name="Super Trusted")  # posts on specific channel according to role
        role2 = discord.utils.get(ctx.guild.roles, name="Trusted")  # if no role regular market
        embed = Embed(color = 16711680)  # SELL NOTIFICATION CODE

        async def send(ctx, channel):
            channel_id = channel
            embed.add_field(name="**A new username has been found in the marketplace.**",
                            value=f"Seller: <@{ctx.author.id}> AKA {ctx.author.name}#{ctx.author.discriminator}")
            embed.add_field(name=f"**Username**:", value=f" @{username}", inline=False)
            embed.add_field(name="**C/O**", value="$0", inline=True)
            embed.add_field(name="**BIN**:", value=f"${str(bin_price)}", inline=True)
            embed.add_field(name="**A note from the seller**:", value=f"{note}", inline=False)
            await self.client.get_channel(channel_id).send(embed=embed)

        if role1 in roles:
            await send(ctx=ctx, channel=807957694690230282)
        elif role2 in roles:
            await send(ctx=ctx, channel=802686271813058601)
        else:
            await send(ctx=ctx, channel=802686273009483776)

        bin_price = int(bin_price)
        people_in_budget = cmj.execute(
            "SELECT budget_people.user_id, budget_people.budget FROM budget_people WHERE budget >= :bin",
            {"bin": int(bin_price)}).fetchall()
        embed = Embed(color = 16711680)
        for i in people_in_budget:
            user_id = i[0]
            embed.add_field(name="A new username in the marketplace is in your budget.",
                            value="A new user has "  # BUDGET DM FEATURE
                                  "been found which "  # If person budget is registered
                                  "is in your "  # and user is under the budget sends a dm
                                  "budget of: {}. "
                                  "The username is "
                                  "**@{}**. Price: ${} .Type "
                                  "!help in "
                                  "#bot-spam (NJ "
                                  "server) to learn "
                                  "more about how "
                                  "you can offer "
                                  "on/b the "
                                  "username.".format(
                                i[1], username, str(bin_price)))
            embed.set_footer(text="Bot coded by: mj#0081 | @maij\t\tng#1990 | @n0e1")

            # incase user leaves the server, and bot cant send message removes the user_id
            try:

                    await self.client.get_user(int(user_id)).send(embed=embed)
            except:
                cmj.execute("DELETE FROM budget_people WHERE user_id=:user_id", {"user_id": user_id})
            embed = Embed(color = 16711680)

    except Exception as error101:
        print(error101)
        await ctx.send('There has been as error using')
    mj_market.close()


class Market(commands.Cog):

    def __init__(self, client):
        self.client = client

    # giveaway
    claimed = False

    @commands.command(pass_context=True,
                      description="Use this command to sell a username in the marketplace. Example: !sell maij 50 uncreated oge, bitcoin accepted. Only instagram usernames can be sold using this.")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def sell(self, ctx, username, bin_price=None, *note):  # arguments, username, bin, note *required*
        if "https://" in username:
            code = username[21:]
            usernames = requests.get(f"https://pastebin.com/raw/{code}").text.split("\r\n")

            for line in usernames:
                line_split = line.split(":")
                username = line_split[0]
                if len(username) > 30:
                    await ctx.send(f"@{username} is over 30 characters long. Please remove it before trying again.")
                    return
                price = line_split[1]
                note = line_split[2]

                await _sell(self, ctx, username, price, note)
        else:
            if bin_price is not None and note is not None:
                note = str(note).replace("'", "").replace(",", "").replace("(", "").replace(")", "")
                if len(username) > 30:
                    await ctx.send(f"@{username} is over 30 characters long. Please remove it before trying again.")
                    return
                await _sell(self, ctx, username, bin_price, note)


            else:
                await ctx.send("There was an error using this command. Please add a bin price and a note.")

    @commands.command(pass_context=True,
                      description="Use this command after you have sold a username you own. Example: !sold n0e1")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def sold(self, ctx, username_sold):
        # sold command - only seller can access
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        global claimed
        username_sold = username_sold.lower()
        seller_ids = ctx.message.author.id  # get messager id person doing !sold
        try:
            if username_sold == None:
                print('error')


            else:

                cmj.execute("DELETE FROM mjmarket WHERE username = :username AND seller_name = :seller_name",
                            # AND TO CHECK OTHERS CANT DELETE
                            {'username': username_sold,
                             'seller_name': seller_ids})  # tries to delete @if seller_name from !sell is same as the person  trying to do !sold
                mj_market.commit()
                if cmj.rowcount == 1:  # if none deleted
                    await ctx.message.add_reaction('✅')
                    embed = Embed(color = 16711680)
                    embed.add_field(name=f"**@{username_sold}** has been sold! ",
                                    value=f"Seller: @{ctx.author.name}#{ctx.author.discriminator}")
                    await self.client.get_channel(807961382561251338).send(embed=embed)
                else:
                    embed = Embed(color = 16711680)
                    embed.add_field(name='i smell something fishy',
                                    value="...trying to figure out how you've sold an @ you don't own.")
                    embed.set_image(url='https://media1.giphy.com/media/4pMX5rJ4PYAEM/giphy.gif')
                    await ctx.send(embed=embed)


        except Exception as error101:
            print(error101)
            await ctx.send('There has been an error using the !sold command')
        mj_market.close()

    @commands.command(pass_context=True,
                      description="Admin command - Use this command to delete a username from the marketplace. Example: !delete maij")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def delete(self, ctx, username_sold):
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        username_sold = username_sold.lower()
        try:
            cmj.execute("DELETE FROM mjmarket WHERE username = :username",  # ADMIN COMMAND TO DELETE/FILTE DB
                        {'username': username_sold})
            mj_market.commit()
            if cmj.rowcount == 1:
                await ctx.message.add_reaction('✅')
        except Exception as error101:
            print(error101)
            await ctx.send('There was an error deleting the username.')
        mj_market.close()

    # SEARCH QUERY FOR USERNAME IN DB
    @commands.command(pass_context=True, name="search", description="This command allows you to search for SPECIFIC "
                                                                    "usernames in the market. Here's some exaples on "
                                                                    "how to use them:\n "
                                                                    "1. ("
                                                                    "!search ms%) will return all the usernames in "
                                                                    "the market that start with the letters ms.\n "
                                                                    "2. ("
                                                                    "!search x+++) will return all usernames that "
                                                                    "contain 4 letters/chars and begin with x.\n "
                                                                    "3. ("
                                                                    "!search w++w) will replace the + signs with "
                                                                    "letters/chars and return usernames if any are "
                                                                    "found.\n "
                                                                    "4. ("
                                                                    "!search w%) returns all usernames that begin "
                                                                    "with w.\n "
                                                                    "5. ("
                                                                    "!search all n) will return all usernames that "
                                                                    "CONTAIN the letter n.\n "
                                                                    "6. (!search ++++ 60) will return all usernames with a length of 4 which are under $60 in price.")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def search(self, ctx, username, letter_all=None):
        global claimed
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        try:
            if letter_all is None:
                letter_all = "0"
            if len(letter_all) > 1:
                username1 = ""
                for char in username:
                    if char == "+":
                        username1 += "_"
                    else:
                        username1 += char
                try:
                    users = cmj.execute(
                        "SELECT mjmarket.username, mjmarket.binprice FROM mjmarket WHERE username LIKE :username AND binprice <= :binprice ORDER BY mjmarket.binprice DESC",
                        {"username": username1, "binprice": int(letter_all)}).fetchall()
                    print(users)
                except Exception as e:
                    print(e)
                    return

                embed = Embed(color = 16711680)
                amount_found = len(users)
                list_of_user = users
                number_of_pages = len(list_of_user) // 24
                remainder = len(list_of_user) % 24
                if remainder != 0:
                    number_of_pages = number_of_pages + 1
                pages_sent = 1
                index = 0
                loops = 0

                embed.set_title(title=f'**Amount of usernames found: {amount_found}**')
                while pages_sent <= number_of_pages:
                    loops += 1
                    if loops == 1:
                        list_of_user = list_of_user[index:]
                    else:
                        list_of_user = list_of_user[index + 1:]
                    for single_user in list_of_user:

                        index = list_of_user.index(single_user)

                        counter = index
                        binprice = single_user[1]
                        user = single_user[0]

                        embed.add_field(name=f"**@{user}**", value=f"${binprice}")
                        counter += 1
                        if counter >= 24: break
                    embed.set_footer(
                        text='Bot Made By : mj#0081 | @maij             ng#1990 | @n0e1\nPage number: ' + str(
                            pages_sent))
                    pages_sent += 1
                    await ctx.author.send(embed=embed)
                    sleep(0.7)
                    embed = Embed(color = 16711680)

                    await ctx.message.add_reaction("✅")

            elif username == "all" and len(letter_all) == 1:
                sql_letter_format = f"%{letter_all}%"
                try:
                    users = cmj.execute(
                        "SELECT mjmarket.username, mjmarket.binprice FROM mjmarket WHERE username LIKE :username ORDER BY mjmarket.binprice DESC",
                        {"username": sql_letter_format}).fetchall()
                except Exception as e:
                    print(e)
                    return
                embed = Embed(color = 16711680)
                amount_found = len(users)
                list_of_user = users
                number_of_pages = len(list_of_user) // 24
                remainder = len(list_of_user) % 24
                if remainder != 0:
                    number_of_pages = number_of_pages + 1
                pages_sent = 1
                index = 0
                loops = 0

                embed.set_title(title=f'**Amount of usernames found: {amount_found}**')
                while pages_sent <= number_of_pages:
                    loops += 1
                    if loops == 1:
                        list_of_user = list_of_user[index:]
                    else:
                        list_of_user = list_of_user[index + 1:]
                    for single_user in list_of_user:

                        index = list_of_user.index(single_user)

                        counter = index
                        binprice = single_user[1]
                        user = single_user[0]

                        embed.add_field(name=f"**@{user}**", value=f"${binprice}")
                        counter += 1
                        if counter >= 24: break
                    embed.set_footer(
                        text='Bot Made By : mj#0081 | @maij             ng#1990 | @n0e1\nPage number: ' + str(
                            pages_sent))
                    pages_sent += 1
                    await ctx.author.send(embed=embed)
                    sleep(0.7)
                    embed = Embed(color = 16711680)

                    await ctx.message.add_reaction("✅")

            elif "+" in username and "%" not in username:
                username1 = ""
                for char in username:
                    if char == "+":
                        username1 += "_"
                    else:
                        username1 += char
                users = cmj.execute(
                    "SELECT mjmarket.username, mjmarket.binprice FROM mjmarket WHERE username LIKE :username ORDER BY mjmarket.binprice DESC",
                    {"username": username1}).fetchall()
                if len(users) == 0:
                    embed = Embed(color = 16711680)
                    embed.add_field(name='No usernames found.',
                                    value="This server is broke. We have no found any usernames that match your queries.")
                    await ctx.send(embed=embed)
                    return
                embed = Embed(color = 16711680)
                amount_found = len(users)
                list_of_user = users
                number_of_pages = len(list_of_user) // 24
                remainder = len(list_of_user) % 24
                if remainder != 0:
                    number_of_pages = number_of_pages + 1
                pages_sent = 1
                index = 0
                loops = 0

                embed.set_title(title=f'**Amount of usernames found: {amount_found}**')
                while pages_sent <= number_of_pages:
                    loops += 1
                    if loops == 1:
                        list_of_user = list_of_user[index:]
                    else:
                        list_of_user = list_of_user[index + 1:]
                    for single_user in list_of_user:

                        index = list_of_user.index(single_user)

                        counter = index
                        binprice = single_user[1]
                        user = single_user[0]

                        embed.add_field(name=f"**@{user}**", value=f"${binprice}")
                        counter += 1
                        if counter >= 24: break
                    embed.set_footer(
                        text='Bot Made By : mj#0081 | @maij             ng#1990 | @n0e1\nPage number: ' + str(
                            pages_sent))
                    pages_sent += 1
                    await ctx.author.send(embed=embed)
                    sleep(0.7)

                    embed = Embed(color = 16711680)

                    await ctx.message.add_reaction("✅")

            elif "%" in username and "_" not in username:
                username1 = ""
                for char in username:
                    if char == "%":
                        username1 += char
                        break
                    else:
                        username1 += char
                users = cmj.execute(
                    "SELECT mjmarket.username, mjmarket.binprice FROM mjmarket WHERE username LIKE :username ORDER BY mjmarket.binprice DESC",
                    {"username": username1}).fetchall()
                if len(users) == 0:
                    embed = Embed(color = 16711680)
                    embed.add_field(name='No usernames found.',
                                    value="This server is broke. We have no found any usernames that match your queries.")
                    await ctx.send(embed=embed)
                    return
                embed = Embed(color = 16711680)
                amount_found = len(users)
                list_of_user = users
                number_of_pages = len(list_of_user) // 24
                remainder = len(list_of_user) % 24
                if remainder != 0:
                    number_of_pages = number_of_pages + 1
                pages_sent = 1
                index = 0
                loops = 0

                embed.set_title(title=f'**Amount of usernames found: {amount_found}**')
                while pages_sent <= number_of_pages:
                    loops += 1
                    if loops == 1:
                        list_of_user = list_of_user[index:]
                    else:
                        list_of_user = list_of_user[index + 1:]

                    for single_user in list_of_user:
                        index = list_of_user.index(single_user)
                        counter = index
                        binprice = single_user[1]

                        user = single_user[0]

                        embed.add_field(name=f"**@{user}**", value=f"${binprice}")
                        counter += 1
                        if counter >= 24: break
                    embed.set_footer(
                        text='Bot Made By : mj#0081 | @maij             ng#1990 | @n0e1\nPage number: ' + str(
                            pages_sent))
                    pages_sent += 1
                    await ctx.author.send(embed=embed)
                    sleep(0.7)

                    embed = Embed(color = 16711680)
                await ctx.message.add_reaction("✅")



            else:
                embed = Embed(color = 16711680)
                embed.add_field(
                    "Type (!help search) for more help. Please also make sure you dont use _ and % in one command.",
                    value="This command is meant to be used like this: !search n+++, !search +n+, where + represents any character. Search y% will mean youre looking for usernames that start with y. . Please include + OR % characters for this command to work.")
                await ctx.send(embed=embed)
        except:
            embed = Embed(color = 16711680)
            embed.add_field(name="4'11",
                            value="There was an error using this command. Please notify an admin and tell them how to recreate this issue.")
            await ctx.send(embed=embed)
        mj_market.close()

    @commands.command(pass_context=True,
                      description="This command allows you to look for usernames in the marketplace which are within your budget. Example: !budget 40. To have the bot message you when a new username is in the marketplace, which is within your budget, type !budget 40 dm.")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def budget(self, ctx, budget_price: int, dm=None):
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        global claimed
        try:  # IF DM IS MENTIONED RECORDS USER DATA INTO BUDGET TABLE
            if dm == 'dm':
                db_return = cmj.execute("SELECT budget_people.user_id FROM budget_people WHERE user_id = :user_id",
                                        {"user_id": ctx.message.author.id}).fetchone()
                if db_return is None:  # IF NOT ALREADY LISTED INSERTS ELSE UPDATES
                    cmj.execute("INSERT INTO budget_people(budget, user_id) VALUES (:budget, :user_id)",
                                {"budget": budget_price, "user_id": ctx.message.author.id})
                    mj_market.commit()
                elif len(db_return) == 1:
                    cmj.execute("UPDATE budget_people SET budget =:budget WHERE user_id = :user_id",
                                {"budget": budget_price, "user_id": ctx.message.author.id})
                    mj_market.commit()
            cmj.execute(
                "SELECT mjmarket.username, mjmarket.binprice FROM mjmarket WHERE binprice <= :budget_price ORDER BY mjmarket.binprice DESC",
                {'budget_price': budget_price})  # SEARCHES FOR USERNAME UNDER BUDGET
            tuple_of_user = cmj.fetchall()
            embed = Embed(color = 16711680)
            embed.set_title(title='Username')
            amount_users = len(tuple_of_user)
            embed.set_author(name='#' + str(amount_users) + ' users found in your budget',
                             icon_url='https://upload.wikimedia.org/wikipedia/commons/9/9e/Borat.portrait.png')
            list_of_user = list(tuple_of_user)
            number_of_pages = len(
                list_of_user) // 24  # THIS STRUCTURE OF CODE IS USED TO SPLIT PAGES, DUE TO EMBED ERROR USED IN MYLIST, SEARCH, BUDGET, YOURLIST etc
            remainder = len(list_of_user) % 24
            if remainder != 0:
                number_of_pages = number_of_pages + 1
            #  have the correct number of pages here
            pages_sent = 1
            index = 0
            loops = 0
            while pages_sent <= number_of_pages:
                loops += 1
                if loops == 1:
                    list_of_user = list_of_user[index:]
                else:
                    list_of_user = list_of_user[index + 1:]

                for single_user in list_of_user:
                    index = list_of_user.index(single_user)
                    counter = index
                    single_user = str(single_user)
                    remove_bracket = single_user.replace("'", ' ').replace("(", " ").replace(')', " ")
                    username_selling = remove_bracket.split(',')[0]
                    user_bin_price = remove_bracket.split(',')[1]
                    embed.add_field(name="@" + username_selling.strip(), value=str(user_bin_price.strip()) + '$')
                    counter += 1
                    if counter >= 24: break
                embed.set_footer(
                    text=f'Bot Made By : mj#0081 | @maij             ng#1990 | @n0e1\nPage number: {str(pages_sent)}')
                pages_sent += 1
                await ctx.author.send(embed=embed)
                sleep(0.7)

                await ctx.message.add_reaction("✅")
                embed = Embed(color = 16711680)


        except Exception as error101:
            print(error101)
            await ctx.send('There was an error using the !budget command.')
        mj_market.close()

    @commands.command(pass_context=True,
                      description="This command allows you to check the note that the seller has provided for their usernames. Please always use this before offering/buying a username to ensure you meet the seller's requirements when purchasing the username. Example: !info n0e1")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def info(self, ctx, username):
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        global claimed
        try:  # SEARCHES FOR INFO
            embed = Embed(color = 16711680)
            note = \
                cmj.execute("SELECT mjmarket.note FROM mjmarket WHERE username=:username",
                            {"username": username}).fetchone()[0]
            if note is None:
                note = "Looks like this seller has not provided a note."  # DUE TO OLD LISTINGS, THIS LINE IS IMPORTENT

            embed.add_field(name=f"A note from the seller of @{username}:", value=note)
            await ctx.send(embed=embed)
            chances = randint(1, 200)
            await ctx.message.add_reaction('✅')

        except Exception as error101:
            print(error101)
            await ctx.send('There has been an error using the !Info command')
        mj_market.close()

    @commands.command(pass_context=True,
                      description="This command returns the buy-it-now price the seller has set for their username. Example: !bin maij")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def bin(self, ctx, username):
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        try:  # SEARCHES FOR BINPRICE OF A USER
            bin_price_ = cmj.execute("SELECT mjmarket.binprice FROM mjmarket WHERE username = :username",
                                     {'username': username}).fetchone()
            if not bin_price_:
                embed = Embed(color = 16711680)
                embed.add_field(name="Username not found.",
                                value="Can't seem to find this username. Please use the !budget command to receive usernames within your budget.")
                await ctx.message.add_reaction('✅')
                await ctx.send(embed=embed)
                return
            bin_price = bin_price_[0]
            embed = Embed(color = 16711680)
            embed.add_field(name=f"{choice(sentences)}", value=f"The bin for @{username} is {bin_price}$.")
            await ctx.send(embed=embed)
        except Exception as error101:
            print(error101)
            await ctx.send('There has been an error using the !bin command')
        mj_market.close()

    @commands.command(pass_context=True,
                      description="This command allows you to place your offer on a username. Type !help info before using this. You can pass in the payment method in the end so the seller can be ready when messaging you, if they accept your offer. To use: !offer maij 200 paypal")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def offer(self, ctx, username, new_offer, payment_method="default payment method"):
        await self.client.wait_until_ready()

        try:
            mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
            cmj = mj_market.cursor()
            global claimed  # offer command
            try:
                username = username.lower()
                buyer_ids = ctx.message.author.id
                if '$' in new_offer:  # replaces $
                    new_offer = new_offer.replace('$', '')

                rex = re.compile('[!@#$%^&*()-+={}|":\;<>,?/]')
                search = rex.search(username)
                cmj.execute("SELECT mjmarket.current_offer FROM mjmarket WHERE username = :username",
                            {'username': username})
                hoffer = cmj.fetchone()
                if hoffer is not None:  # checks if user exists
                    highest_offer = hoffer[0]
                    if int(new_offer) > int(
                            highest_offer):  # check if the new offer is higher than old offer, else offer declined
                        cmj.execute("SELECT mjmarket.binprice FROM mjmarket WHERE username = :username",
                                    {'username': username})

                        bnprice = cmj.fetchall()
                        set_bin_price = bnprice[0][0]

                        cmj.execute(
                            "SELECT mjmarket.seller_name, mjmarket.highest_bidder FROM mjmarket WHERE username = :username",
                            {'username': username})

                        info_d = str(cmj.fetchall())
                        info_data_ = info_d.replace("'", '').replace('[', '').replace(']', '').replace('(', '').replace(
                            ')',
                            '')
                        info_seller = int(info_data_.split(',')[0])

                        info_bidder = int(info_data_.split(',')[1])
                        if int(new_offer) < int(set_bin_price):  # checks if offer passes bin price

                            cmj.execute(
                                "UPDATE mjmarket SET current_offer = :new_offer, highest_bidder = :new_buyer WHERE username = :username and current_offer = :highest_offer",
                                {'new_offer': new_offer, 'new_buyer': buyer_ids, 'username': username,
                                 'highest_offer': highest_offer})
                            mj_market.commit()

                            embed = Embed(color = 16711680)  # offer accepted
                            embed.add_field(name=f'Your offer for @{username} has been accepted!',
                                            value='This offer, along with your discord tag,  has been sent to the seller.')

                            await ctx.author.send(embed=embed)
                            embed2 = Embed(color = 16711680)
                            embed2.add_field(name=f'New current offer on your username - @{username}-',
                                             value=f'{new_offer}$ This is the new current offer.')
                            await self.client.get_user(info_seller).send(embed=embed2)  # dms seller
                            await self.client.get_user(info_seller).send(
                                f'New Bidder:  <@{str(buyer_ids)}>  {str(ctx.author.name)}#{str(ctx.author.discriminator)}')
                            if info_bidder != 0:  # check if any pervios co
                                try:
                                    cmj.execute(
                                        "UPDATE mjmarket SET prev_co = :previous_offer, prev_bidder = :previous_bidder WHERE username = :username",
                                        {'previous_offer': highest_offer, 'previous_bidder': info_bidder,
                                         'username': username})
                                    mj_market.commit()

                                    embed3 = Embed(color = 16711680)
                                    embed3.add_field(name='You have been outbid',
                                                     value=f'Your offer for @{username} has been outbid by a new bidder\nIf you would like to purchase this user, Please offer higher.')
                                    await self.client.get_user(info_bidder).send(embed=embed3)
                                except:
                                    cmj.execute("DELETE mjmarket WHERE seller_id = :info_bidder",
                                                {'info_bidder': info_bidder})
                                    cmj.execute(
                                        "UPDATE mjmarket SET prev_co = 0, prev_bidder = 0 WHERE username = :username",
                                        {'username': username})
                                    mj_market.commit()
                            else:
                                no_bidder_b_error_n = 0
                            try:
                                roles = await self.client.get_guild(788462475430461451).fetch_member(info_seller)
                                roles = roles.roles
                                role1 = discord.utils.get(self.client.get_guild(788462475430461451).roles,
                                                          name="Super Trusted")
                                role2 = discord.utils.get(self.client.get_guild(788462475430461451).roles,
                                                          name="Trusted")
                                seller_name_embed = self.client.get_user(info_seller).name
                                seller_num_embed = self.client.get_user(info_seller).discriminator
                            except:
                                traceback.print_exc()

                            async def send(ctx, channel):
                                channel_id = channel
                                embed = Embed(color = 16711680)
                                embed.add_field(name=f"**A new offer has been placed on @{username}!**",
                                                value=f"Use !offer to place your offers or !buy to purchase this username!")
                                embed.add_field(name=f"**Username**:", value=f" @{username}", inline=False)
                                embed.add_field(name="**C/O**", value=f"{str(new_offer)}", inline=True)
                                embed.add_field(name="**BIN**:", value=f"${str(set_bin_price)}", inline=True)
                                await self.client.get_channel(channel_id).send(embed=embed)

                            if role1 in roles:
                                await send(ctx=ctx, channel=807957694690230282)
                            elif role2 in roles:
                                await send(ctx=ctx, channel=802686271813058601)
                            else:
                                await send(ctx=ctx, channel=802686273009483776)
                            embed = Embed(color = 16711680)
                            embed.add_field(name=f"**A new offer has been placed on @{username}!**",
                                            value=f"Use !offer to place your offers or !buy to purchase this username!")
                            embed.add_field(name=f"**Username**:", value=f" @{username}", inline=False)
                            embed.add_field(name="**C/O**", value=f"{str(new_offer)}", inline=True)
                            embed.add_field(name="**BIN**:", value=f"${str(set_bin_price)}", inline=True)
                        else:

                            cmj.execute(
                                "UPDATE mjmarket SET current_offer = :new_offer, highest_bidder = :new_buyer WHERE username = :username and current_offer = :highest_offer",
                                {'new_offer': new_offer, 'new_buyer': buyer_ids, 'username': username,
                                 'highest_offer': highest_offer})
                            embed = Embed(color = 16711680)
                            embed.add_field(name='Your offer has been accepted.',
                                            value=f'You currently hold the highest bid on @{username}.\nThe seller has been notified of your discord tag and offer.')
                            embed2 = Embed(color = 16711680)
                            embed2.add_field(name=f'New Offer: {new_offer}$',
                                             value=f'The newest offer on your user - @{username} - has passed the bin price. Please contact the buyer in order to complete the deal. He/she is looking to buy the username using {payment_method}')

                            await ctx.author.send(embed=embed)
                            await ctx.author.send(
                                f"Seller:  <@{str(info_seller)}> AKA {self.client.get_user(info_seller).name}#{self.client.get_user(info_seller).discriminator}")
                            await self.client.get_user(info_seller).send(embed=embed2)
                            await self.client.get_user(info_seller).send(
                                f'Buyer:  <@{buyer_ids}>  AKA {self.client.get_user(buyer_ids).name}#{self.client.get_user(buyer_ids).discriminator}')
                            mj_market.commit()

                    else:

                        embed = Embed(color = 16711680)  # offer declined
                        embed.add_field(name=f'Your offer for @{username} has been declined!',
                                        value=f'Current offer: {highest_offer}$\nPlease use the !co command to find the highest current offer on a specific username.')
                        await ctx.author.send(embed=embed)
                        await ctx.message.add_reaction("❌")
                        return
                else:

                    embed = Embed(color = 16711680)  # user not exists
                    embed.add_field(name='Username not found.',
                                    value='The user you tried to offer is not listed for sale\nPlease use the !budget/!exist command to find the users listed in the bot.')
                    await ctx.send(embed=embed)

            except Exception as error101:
                print(error101)
                await ctx.send('There has been an error using the !offer command')
            mj_market.close()
        except Exception as e:
            traceback.print_exc()

    @commands.command(pass_context=True,
                      description="This command displays all the usernames you have for sale. Example: !mylist")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def mylist(self, ctx):
        if str(ctx.channel) == "english-channel" or str(ctx.channel) == "arab-channel":
            embed = Embed(color = 16711680)
            embed.add_field(name="Please do not use this command in a public chat!",
                            value="Use this command in #bot-spam or the marketplace.")
            await ctx.send(embed=embed)
            return
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        global claimed
        instagram_link = "https://instagram.com/"
        telegram = "https://t.me/"
        oguu_link = "https://ogusers.com/"
        kik_link = "https://kik.me/"
        ogx_link = "https://ogx.gg/"
        tiktok_link = "https://tiktok.com/@"
        try:
            seller_id = ctx.message.author.id
            cmj.execute(
                "SELECT mjmarket.username, mjmarket.binprice, mjmarket.current_offer FROM mjmarket WHERE seller_name=:seller_id ORDER BY mjmarket.binprice DESC",
                {"seller_id": seller_id})
            users = cmj.fetchall()
            if str(users) == '[]':  # if user has not listed in our bot
                embed = Embed(color = 16711680)
                embed.add_field(name='00ps - l00ks like there was an issue displaying your list.',
                                value='You have no users listed !help sell')
                return_ctx = await ctx.send(embed=embed)
                msg = await ctx.channel.fetch_message(return_ctx.id)

                await asyncio.sleep(30)
                await msg.delete()
                await ctx.message.delete()
                return

            username_list = []  # creates a local list of username person ownss
            for user_tuple in users:
                username_list.append(user_tuple)
            embed = Embed(color = 16711680)
            embed.set_title(title=f"{ctx.author}'s username(s) are:")
            list_of_user = username_list
            number_of_pages = len(
                list_of_user) // 24  # THIS STRUCTURE OF CODE IS USED TO SPLIT PAGES, DUE TO EMBED ERROR USED IN MYLIST, SEARCH, BUDGET, YOURLIST etc
            remainder = len(list_of_user) % 24
            if remainder != 0:
                number_of_pages = number_of_pages + 1
            #  have the correct number of pages here
            pages_sent = 1  # base value
            index = 0
            loops = 0
            list_no = 1
            status = 0
            while pages_sent <= number_of_pages:
                if pages_sent == 1:
                    list_no = 1
                else:
                    list_no = pages_sent * 24 - 24
                loops += 1
                if loops == 1:
                    list_of_user = list_of_user[index:]  # checking for index where to start
                else:
                    list_of_user = list_of_user[index + 1:]

                for item in list_of_user:
                    index = list_of_user.index(item)  # position of user
                    counter = index

                    username = item[0]  # details on each user, username, co , bin
                    price = item[1]
                    current_offer = item[2]
                    counter += 1
                    embed.add_field(name="{}. @{}".format(list_no + index, username),
                                    # incase of more than one embed send, fixes numbering of @/listing number
                                    value="C/O: ${}\a\a BIN: ${}".format(current_offer, price), inline=True)
                    if counter >= 24: break
                try:
                    accounts = cmj.execute("SELECT * FROM socialmedia WHERE member_id = :member",
                                           {'member': ctx.author.id}).fetchone()
                    list_of_socials = {"2": "Discord", "3": "Instagram", "4": "Telegram", "5": "OGU", "6": "Kik",
                                       "7": "Tiktok", "8": "OGX"}

                    loop_no = 0
                    list_accounts = []
                    new_list = []
                    for account in accounts:
                        loop_no += 1
                        list_accounts.append((account, loop_no))
                    for i in range(7):
                        username = list_accounts[i][0]
                        if username != "N/A":
                            new_list.append(list_accounts[i])

                    embed1 = Embed(color = 16711680)

                    for i in new_list:
                        try:
                            if list_of_socials[str(i[1])] == "Instagram":

                                user = f"[{i[0]}]({instagram_link}{i[0]})"
                                embed1.add_field(name=f"{list_of_socials[str(i[1])]}:", value=f"{user}", inline=True)
                            elif list_of_socials[str(i[1])] == "Telegram":

                                user = f"[{i[0]}]({telegram}{i[0]})"
                                embed1.add_field(name=f"{list_of_socials[str(i[1])]}:", value=f"{user}", inline=True)
                            elif list_of_socials[str(i[1])] == "OGU":

                                user = f"[{i[0]}]({oguu_link}{i[0]})"
                                embed1.add_field(name=f"{list_of_socials[str(i[1])]}:", value=f"{user}", inline=True)
                            elif list_of_socials[str(i[1])] == "OGX":

                                user = f"[{i[0]}]({ogx_link}{i[0]})"
                                embed1.add_field(name=f"{list_of_socials[str(i[1])]}:", value=f"{user}", inline=True)
                            elif list_of_socials[str(i[1])] == "Kik":

                                user = f"[{i[0]}]({kik_link}{i[0]})"
                                embed1.add_field(name=f"{list_of_socials[str(i[1])]}:", value=f"{user}", inline=True)
                            elif list_of_socials[str(i[1])] == "Tiktok":
                                user = f"[{i[0]}]({tiktok_link}{i[0]})"
                                embed1.add_field(name=f"{list_of_socials[str(i[1])]}:", value=f"{user}", inline=True)

                            else:
                                embed1.add_field(name=f"{list_of_socials[str(i[1])]}:", value=f"{i[0]}", inline=True)
                        except:
                            pass

                except Exception as e:
                    print(e)
                    status = 1
                embed.set_footer(
                    text=f'Bot Made By : mj#0081 | @maij             ng#1990 | @n0e1\nPage number: {str(pages_sent)}')
                pages_sent += 1
                await ctx.send(embed=embed)
                sleep(0.7)
                if status != 1:
                    await ctx.send(embed=embed1)

                await ctx.message.add_reaction("✅")
                embed = Embed(color = 16711680)


        except Exception as error101:
            print(error101)
            await ctx.send('There has been an error using the !mylist command')
        mj_market.close()
        await asyncio.sleep(10)
        await ctx.message.delete()

    @commands.command(pass_context=True,
                      description="Admin command - This command returns the highest bidder on a username. Example: !findbidder n0e1")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def findbidder(self, ctx, username):
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        try:
            offerer = cmj.execute(
                "SELECT mjmarket.highest_bidder, mjmarket.current_offer FROM mjmarket WHERE username=:username",
                {"username": username}).fetchone()
            if offerer is None:
                await ctx.author.send("No one has offered on @{} yet.".format(username))
            else:
                await ctx.author.send(
                    f"The highest bidder on @{username} is <@{offerer[0]}> with an offer of ${offerer[1]} ")
            await ctx.message.add_reaction('✅')
        except Exception as error101:
            print(error101)
            await ctx.send('There has been an error using the !findbidder command')
        mj_market.close()
################################################# done till buy
    @commands.command(pass_context=True,
                      description="This command allows you to buy a username for the bin price. To use: !buy maij btc. To check the bin, type !help bin.")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def buy(self, ctx, username, payment_method=None):
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        global claimed, available_mm
        try:
            buyer_info_id = ctx.message.author.id
            if payment_method is None:  # PAYMENT METHOD REQUIRED
                embed = Embed(color = 16711680)
                embed.add_field(name="@disqualificationified 50$ mj/ng mm lmk :rofl:",
                                value="Please add a payment method in the end! \nExample: !buy disqualificationified paypal. \nMAKE SURE TO CHECK WHAT PAYMENT"
                                      " METHODS THE SELLER IS ACCEPTING USING !info disqualificationified")
                await ctx.send(embed=embed)
                return
            db_bin_sid = cmj.execute("SELECT mjmarket.seller_name FROM mjmarket WHERE username=:username",
                                     {"username": username}).fetchone()
            if db_bin_sid is None:  # IF USER IS NOT LISTED
                embed = Embed(color = 16711680)
                embed.add_field(name="Username not found.",
                                value="The username you are trying to buy is not available. Please type !help budget to look for usernames in your budget.")
                await ctx.send(embed=embed)
                return

            seller_id = int(db_bin_sid[0])
            db_bin_price = cmj.execute("SELECT mjmarket.binprice FROM mjmarket WHERE username=:username",
                                       {"username": username})
            bin_price = int(db_bin_price.fetchone()[0])
            # UPDATES BIN
            cmj.execute(
                "UPDATE mjmarket SET highest_bidder = :buyer_id, current_offer = :co WHERE username= :username",
                {"buyer_id": ctx.message.author.id, "co": int(bin_price), "username": username})
            mj_market.commit()
            # SENDS BUYER THE SELLER, TO CHOOSE MM OR NOT
            vouches = cmj.execute("SELECT vouches.vouch_number FROM vouches WHERE seller_id=:seller_id",
                                  {"seller_id": seller_id}).fetchone()
            if vouches is None:
                rep_seller = 0
            else:
                rep_seller = vouches[0]
            role1 = discord.utils.get(self.client.get_guild(788462475430461451).roles,
                                      name="Super Trusted")  # posts on specific channel according to role
            role2 = discord.utils.get(self.client.get_guild(788462475430461451).roles, name="Trusted")
            seller_role = await self.client.get_guild(788462475430461451).fetch_member(seller_id)
            seller_role = seller_role.roles
            if role1 in seller_role:
                role = "super trusted"
            else:
                if role2 in seller_role:
                    role = "trusted"
                else:
                    role = "not trusted enough in NJ server. We recommend using a middleman unless you have dealt with this person before."
            if int(rep_seller) < 0:
                emoji = ":exclamation::exclamation:"
            else:
                emoji = " ✅"
            if role[0] == "n":
                embed = Embed(color = 16711680)
                embed.add_field(
                    name=f"The seller of @{username} is: <@{seller_id}>. AKA {self.client.get_user(seller_id).name}#{self.client.get_user(seller_id).discriminator}.",
                    value=f"\nCurrent vouches = {rep_seller}{emoji}\nThis member is {role}")
                await ctx.author.send(embed=embed)
            else:
                embed = Embed(color = 16711680)
                embed.add_field(
                    name=f"The seller of @{username} is: <@{seller_id}>. AKA {self.client.get_user(seller_id).name}#{self.client.get_user(seller_id).discriminator}.",
                    value=f"\nCurrent vouches = {rep_seller}{emoji}\nThis member is {role} in MJ server.")
                await ctx.author.send(embed=embed)

            embed = Embed(color = 16711680)
            embed.add_field(name="Choice:",
                            value="\nWould You like to use a middleman?\nIf yes, type (!mm)\nIf not just ignore this message. \nYou have 45 seconds to decide.")
            await ctx.author.send(embed=embed)

            def check(m):
                return m.content == '!mm' and ctx.author.id == m.author.id

            # USES ASYNCIO.WAIT_FOR if person types !mm or not
            try:
                msg = await self.client.wait_for('message', timeout=45.0, check=check)
            except asyncio.TimeoutError:  # else no mm
                await ctx.author.send('You have chosen not to use a middleman.')
                await self.client.get_user(int(seller_id)).send(
                    f"<@{ctx.message.author.id}> ({ctx.author.name}#{ctx.author.discriminator}) wants to buy @{username} from you for the bin price! Contact him to make a deal. He/she is looking to buy the username using {payment_method}.")
                embed = Embed(color = 16711680)
                embed.add_field("Process done ✅",
                                value="The seller has been notified - please wait until he contacts you so you can make a deal. Check #middlemen if you need a middleman.")
                await ctx.author.send(embed=embed)

            else:  # if mm option chosen
                await ctx.author.send('You have chosen to use a middleman. Finding available middlemen.')

                mm_role = discord.utils.get(self.client.get_guild(788462475430461451).roles, name="middleman")
                online_mms = []
                idle_mms = []
                dnd_mms = []
                print(online_mms)

                for member in self.client.get_guild(788462475430461451).members:
                    if mm_role in member.roles and str(member.status) == "online":
                        online_mms.append(member)
                for member in self.client.get_guild(788462475430461451).members:
                    if mm_role in member.roles and str(member.status) == "idle":
                        idle_mms.append(member)
                for member in self.client.get_guild(788462475430461451).members:
                    if mm_role in member.roles and str(member.status) == "dnd":
                        dnd_mms.append(member)
                available_mm = 0
                print('reached')
                nj_status = self.client.get_guild(788462475430461451).get_member(508073794997452813)
                nj_status = nj_status.status
                ng_status = self.client.get_guild(788462475430461451).get_member(443398625624588299)
                ng_status = ng_status.status
                print(ng_status)

                if str(nj_status) == "online":
                    available_mm = 508073794997452813
                elif str(ng_status) == "online":
                    available_mm = 443398625624588299
                else:
                    def find_mm(list_of_mms):
                        mm_found = False
                        while not mm_found:
                            try:
                                mm = choice(list_of_mms)
                                available_mm = mm.id
                                print(available_mm)
                                return available_mm
                            except Exception as e:
                                print(e)

                                available_mm = 0
                                return available_mm

                    step_1 = find_mm(online_mms)
                    if step_1 == 0:
                        step_2 = find_mm(idle_mms)
                        if step_2 == 0:
                            step_3 = find_mm(dnd_mms)
                            if step_3 == 0:
                                available_mm = 508073794997452813

                            else:
                                available_mm = step_3
                        else:
                            available_mm = step_2
                    else:
                        available_mm = step_1

                overwrites = {  # CREATES A PRIVATE CHANNEL IN GUILDS
                    self.client.get_guild(788462475430461451).default_role: discord.PermissionOverwrite(
                        view_channel=False),
                    self.client.get_guild(788462475430461451).get_member(
                        int(buyer_info_id)): discord.PermissionOverwrite(read_messages=True),
                    self.client.get_guild(788462475430461451).get_member(
                        int(seller_id)): discord.PermissionOverwrite(read_messages=True),
                    self.client.get_guild(788462475430461451).get_member(
                        int(available_mm)): discord.PermissionOverwrite(read_messages=True)
                }
                cc = await self.client.get_guild(788462475430461451).create_text_channel('mm-channel-' + username,
                                                                                         overwrites=overwrites)  # CREATES CHANNEL AND PINGS PEOPLE
                await self.client.get_channel(int(cc.id)).send(
                    f'Buyer: <@{buyer_info_id}>\t\tSeller: <@{seller_id}>\t\tMM: <@{available_mm}>\nUsername: {username}')
                await self.client.get_user(int(seller_id)).send(
                    f' <@{buyer_info_id}> wants to buy @{username} from you. He has chosen to use a middleman. Please check MJ server.')

        except Exception as error101:
            print(error101)
            await ctx.send('There has been an error using the !buy command')
        mj_market.close()
        await ctx.message.add_reaction('✅')

    @commands.command(pass_context=True,
                      description="This command allows you to check the highest offer on a username for the bin price. To use: !co n0e1")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def co(self, ctx, username):
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        global claimed  # RETURNS CURRENT CO OF USER
        try:
            c_o = cmj.execute("SELECT mjmarket.current_offer FROM mjmarket WHERE username=:username",
                              {"username": username}).fetchone()
            if c_o is None:
                embed = Embed(color = 16711680)
                embed.add_field(name="Username not found.",
                                value="Can't seem to find this username. Please use the !budget command to receive usernames within your budget.")
                await ctx.send(embed=embed)
                return
            c_o = c_o[0]
            embed = Embed(color = 16711680)
            embed.add_field(name=f"{choice(sentences)}", value=f"The highest offer for @{username} is {c_o}$.")
            await ctx.send(embed=embed)

        except Exception as error101:
            print(error101)
            await ctx.send('There has been an error using the !co command')
        mj_market.close()

    @commands.command(pass_context=True,
                      description="Admin command - This command returns the seller of a username. Example: !findbidder n0e1")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def findseller(self, ctx, username):
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        try:
            user_id = cmj.execute("SELECT mjmarket.seller_name FROM mjmarket WHERE username=:username",
                                  {"username": username}).fetchone()[0]
            await ctx.author.send(f"Owner of @{username}: <@{user_id}>")
            await ctx.message.add_reaction('✅')
        except Exception as error101:
            print(error101)
            await ctx.send('There has been an error using the !findseller command')
        mj_market.close()

    @commands.command(pass_context=True,
                      description="This command allows you to update the buy-it-now price of a username. Example: !update maij 50")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def update(self, ctx, username, bin_price: int, *, note):
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        try:  # UPDATE COMMAND, INSTEAD OF SOLD
            if len(note) == 0:
                embed = Embed(color = 16711680)
                embed.add_field(name="Please add a note!",
                                value="Please add a note to the buyers. !sell maij 50 comes with oge, pp and btc accepted.")
                await ctx.send(embed=embed)
                return
            user_id = ctx.message.author.id
            user = cmj.execute("SELECT mjmarket.seller_name from mjmarket WHERE username= :username",
                               {"username": username}).fetchone()
            if user is None or int(user[0]) != user_id:
                embed = Embed(color = 16711680)
                embed.add_field(name="you **naughty** naughtyy", value="You do not own this username.")
                await ctx.send(embed=embed)
            else:
                note = str(note).replace("'", "").replace(",", "").replace("(", "").replace(")", "")
                cmj.execute("UPDATE mjmarket SET binprice=:binprice, note = :note WHERE username = :username",
                            {"binprice": bin_price, "note": note, "username": username})
                mj_market.commit()
                await ctx.message.add_reaction("✅")
        except Exception as error101:
            print(error101)
            await ctx.send('There has been an error using the !update command')
        mj_market.close()

    @commands.command(pass_context=True,
                      description="This command allows you to reset all information the bot has stored on a username you're selling. That means that: C/O, highest bidder, previous bidder, will all be deleted, and only the BIN remains. Example: !reset n0e1")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def reset(self, ctx, username):
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        try:
            user_id = ctx.message.author.id
            user = cmj.execute("SELECT mjmarket.seller_name from mjmarket WHERE username= :username",
                               {"username": username}).fetchone()
            if user is None or int(user[0]) != user_id:
                embed = Embed(color = 16711680)
                embed.add_field(name='what are you doing?',
                                value='You are not selling this username. Use !mylist to find your list')
                await ctx.send(embed=embed)
            else:
                cmj.execute(
                    "UPDATE mjmarket SET current_offer = 0, highest_bidder = 0, prev_co = 0, prev_bidder = 0 WHERE username = :username",
                    {'username': username})
                mj_market.commit()
                await ctx.message.add_reaction("✅")
        except Exception as error101:
            await ctx.send('There has been an error using the !reset command')
        mj_market.close()

    @commands.command(pass_context=True,

                      description="This command allows you to reset the current offer on a username to the previous offer. This is to be used when someone has fake offered on your username. Example: !resetco maij ")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def resetco(self, ctx, username):
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        try:  # reser co
            user_id = ctx.message.author.id
            user = cmj.execute("SELECT mjmarket.seller_name from mjmarket WHERE username= :username",
                               {"username": username}).fetchone()
            if user is None or int(user[0]) != user_id:
                embed = Embed(color = 16711680)
                embed.add_field(name='MG-BOT > OGU',
                                value='You are not selling this username. Use !mylist to find your list')
                await ctx.send(embed=embed)
            else:
                cmj.execute(
                    "UPDATE mjmarket SET current_offer = prev_co, highest_bidder = prev_bidder, prev_co = 0, prev_bidder = 0 WHERE username= :username",
                    {'username': username})
                mj_market.commit()
                await ctx.message.add_reaction("✅")
        except Exception as error101:
            print(error101)
            await ctx.send('There has been an error using the !resetcos command')
        mj_market.close()

    @commands.command(pass_context=True, description="This command tells you whether a username is for sale.")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def exist(self, ctx, username):
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        try:  # check if user exists
            results = cmj.execute("SELECT username FROM mjmarket WHERE username = :username",
                                  {'username': username}).fetchone()
            if not results:
                embed = Embed(color = 16711680)
                embed.add_field(name='crazy.',
                                value=' This username is not listed for sale in the marketplace.')
                await ctx.send(embed=embed)
                return
            embed = Embed(color = 16711680)
            embed.add_field(name='www.bing.com', value='This username is for sale in the marketplace.')
            await ctx.send(embed=embed)
        except Exception as error101:
            print(error101)
            await ctx.send('There has been an error using the !exist command')
        mj_market.close()

    @commands.command(pass_context=True, name="yourlist",
                      description="This command displays all the usernames someone has for sale.")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def yourlist(self, ctx, member: discord.Member):
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        global claimed
        try:
            member_id = member.id
            cmj.execute(
                "SELECT mjmarket.username, mjmarket.binprice, mjmarket.current_offer FROM mjmarket WHERE seller_name=:seller_id",
                {"seller_id": member_id})
            users = cmj.fetchall()
            if str(users) == '[]':  # if user has not listed in our bot
                embed = Embed(color = 16711680)
                embed.add_field(name='00ps - l00ks like there was an issue displaying your list.',
                                value='You have no users listed !help sell')
                await ctx.send(embed=embed)
                return
            username_list = []
            for user_tuple in users:
                username_list.append(user_tuple)
            embed = Embed(color = 16711680)
            embed.set_title(title=f"{member.name}#{member.discriminator}'s username(s) are:")
            embed.set_title(title='Username')
            list_of_user = username_list
            number_of_pages = len(list_of_user) // 24
            remainder = len(list_of_user) % 24
            if remainder != 0:
                number_of_pages = number_of_pages + 1
            #  have the correct number of pages here
            pages_sent = 1
            index = 0
            loops = 0
            list_no = 1
            while pages_sent <= number_of_pages:
                if pages_sent == 1:
                    list_no = 1
                else:
                    list_no = pages_sent * 24 - 24
                loops += 1
                if loops == 1:
                    list_of_user = list_of_user[index:]
                else:
                    list_of_user = list_of_user[index + 1:]

                for item in list_of_user:
                    index = list_of_user.index(item)
                    counter = index

                    username = item[0]
                    price = item[1]
                    current_offer = item[2]
                    # embed.add_field(name=f"{counter}. ", value="@" + username, inline=True)
                    # messages_str += "{}. @{}   \a\a\a   C/O: ${}  \a\a\a  BIN: ${}\n".format(counter, username, current_offer, price)
                    counter += 1
                    if loops != 1:
                        embed.add_field(name="{}. @{}".format(list_no + index + 1, username),
                                        value="C/O: ${}\a\a BIN: ${}".format(current_offer, price), inline=True)
                    else:
                        embed.add_field(name="{}. @{}".format(list_no + index, username),
                                        value="C/O: ${}\a\a BIN: ${}".format(current_offer, price), inline=True)
                    if counter >= 24: break
                embed.set_footer(
                    text='Bot Made By : mj#0081 | @maij             ng#1990 | @n0e1\nPage number: ' + str(pages_sent))
                pages_sent += 1
                await ctx.send(embed=embed)
                sleep(0.7)

                await ctx.message.add_reaction("✅")
                embed = Embed(color = 16711680)


        except Exception as error101:
            print(error101)
            await ctx.send('There has been an error using the !yourlist command')
        mj_market.close()

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        member_id = member.id
        cmj.execute("DELETE FROM mjmarket WHERE seller_name = :seller_name", {'seller_name': member_id})
        mj_market.commit()
        cmj.execute("DELETE FROM budget_people WHERE user_id = :delete_user", {'delete_user': member_id})
        mj_market.commit()
        sleep(2)
        cmj.execute("DELETE FROM vouches WHERE seller_id = :delete_user", {'delete_user': member_id})
        mj_market.commit()

        sleep(2)
        cmj.execute("DELETE FROM voucherss WHERE member_id = :delete_user", {'delete_user': member_id})
        mj_market.commit()

        sleep(2)
        cmj.execute("UPDATE mjmarket SET highest_bidder = 0 WHERE highest_bidder = :delete_user",
                    {'delete_user': member_id})
        mj_market.commit()
        mj_market.close()


    @commands.command(name="setsocial",
                      description="Use this command to set your social medias. !setsocial instagram defending, for example. Supported medias: instagram, ogu, tele, kik, tiktok.",
                      pass_context=True)
    async def setsocial(self, ctx, media, account):
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()

        discord_member = ctx.message.author
        check_exist = cmj.execute("SELECT * FROM socialmedia WHERE member_id = :member",
                                  {'member': discord_member.id}).fetchone()
        discord_username = discord_member.name + '#' + discord_member.discriminator
        media = media.lower()

        if media == 'instagram' or media == 'ig' or media == 'insta':
            media = 'instagram'
        elif media == 'telegram' or media == 'tele':
            media = 'telegram'
        elif media == 'ogu' or media == 'ogusers':
            media = 'ogu'
        elif media == 'kik':
            media = 'kik'
        elif media == 'tiktok':
            media = 'tiktok'
        elif media == "ogx":
            media = "ogx"
        else:
            embed = Embed(color = 16711680)
            embed.add_field(name='ohh let me also add your linkedin',
                            value='The social media you chose does not exist.')
            await ctx.send(embed=embed)
            return
        if check_exist is None:
            cmj.execute(
                f"INSERT INTO socialmedia(member_id, discord_user, {media}) VALUES (:member, :discord, :account)",
                {'member': discord_member.id, 'discord': discord_username, 'account': account})
            mj_market.commit()

        else:
            cmj.execute(
                f" UPDATE socialmedia SET discord_user = :discord, {media} = :account WHERE member_id = :member ",
                {'discord': discord_username, 'account': account, 'member': discord_member.id})
            mj_market.commit()
        await ctx.message.add_reaction("✅")
        mj_market.close()

    @commands.command(name="socials",
                      description="Use this command to view your social medias. Use !setsocial to set these.",
                      pass_context=True)
    async def socials(self, ctx, member: discord.Member = None):
        instagram_link = "https://instagram.com/"
        telegram = "https://t.me/"
        oguu_link = "https://ogusers.com/"
        kik_link = "https://kik.me/"
        ogx_link = "https://ogx.gg/"
        tiktok_link = "https://tiktok.com/@"

        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        if member is None:
            member = ctx.author

        discord_member = member.id
        accounts = cmj.execute("SELECT * FROM socialmedia WHERE member_id = :member",
                               {'member': discord_member}).fetchone()

        if accounts is None:
            embed = Embed(color = 16711680)
            embed.set_image(url='https://i.postimg.cc/Nf1QpJ26/image.png')
            embed.add_field(name='ctrl-C + ctrl-V skillz',
                            value='This person has not set up their socials yet. Use the !setsocial command to set your own socials.')
            await ctx.send(embed=embed)
            return

        embed = Embed(color = 16711680)
        embed.set_author(name=f"{accounts[1]}'s socials")

        list_of_socials = {"2": "Discord", "3": "Instagram", "4": "Telegram", "5": "OGU", "6": "Kik",
                           "7": "Tiktok", "8": "OGX"}

        loop_no = 0
        list_accounts = []
        new_list = []
        for account in accounts:
            loop_no += 1
            put_info_list_accounts = [account, loop_no]
            list_accounts.append(put_info_list_accounts)
        
        for i in range(7):
            print(i)
            
            username = list_accounts[i][0]
            if username != "N/A":
                new_list.append(list_accounts[i])

        embed1 = Embed(color = 16711680)

        for i in new_list:
            try:
                if list_of_socials[str(i[1])] == "Instagram":

                    user = f"[{i[0]}]({instagram_link}{i[0]})"
                    embed1.add_field(name=f"{list_of_socials[str(i[1])]}:", value=f"{user}", inline=True)
                elif list_of_socials[str(i[1])] == "Telegram":

                    user = f"[{i[0]}]({telegram}{i[0]})"
                    embed1.add_field(name=f"{list_of_socials[str(i[1])]}:", value=f"{user}", inline=True)
                elif list_of_socials[str(i[1])] == "OGU":

                    user = f"[{i[0]}]({oguu_link}{i[0]})"
                    embed1.add_field(name=f"{list_of_socials[str(i[1])]}:", value=f"{user}", inline=True)
                elif list_of_socials[str(i[1])] == "OGX":

                    user = f"[{i[0]}]({ogx_link}{i[0]})"
                    embed1.add_field(name=f"{list_of_socials[str(i[1])]}:", value=f"{user}", inline=True)
                elif list_of_socials[str(i[1])] == "Kik":

                    user = f"[{i[0]}]({kik_link}{i[0]})"
                    embed1.add_field(name=f"{list_of_socials[str(i[1])]}:", value=f"{user}", inline=True)
                elif list_of_socials[str(i[1])] == "Tiktok":
                    user = f"[{i[0]}]({tiktok_link}{i[0]})"
                    embed1.add_field(name=f"{list_of_socials[str(i[1])]}:", value=f"{user}", inline=True)

                else:
                    embed1.add_field(name=f"{list_of_socials[str(i[1])]}:", value=f"{i[0]}", inline=True)
            except:
                pass

        await ctx.send(embed=embed1)
        mj_market.close()

    @commands.command()
    async def trade(self, ctx, username_trade_request, *trade_deal):
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        if len(trade_deal) == 0:
            embed = Embed(color = 16711680)
            embed.add_field(name="Please specify a deal",
                            value="Please add the specifics of your trade\n!trade maij i want to trade with the insta @mj")
            await ctx.send(embed=embed)
            return
        db_username_exist = cmj.execute("SELECT mjmarket.seller_name FROM mjmarket WHERE username=:username",
                                        {"username": username_trade_request}).fetchone()
        if db_username_exist is None:  # IF USER IS NOT LISTED
            embed = Embed(color = 16711680)
            embed.add_field(name="Username not found.",
                            value="The username you are trying to trade is not available. Please type !help budget to look for usernames in your budget.")
            await ctx.send(embed=embed)
            return

        seller_id = int(db_username_exist[0])
        trade_requester = ctx.message.author
        note = str(trade_deal).replace("'", "").replace(",", "").replace("(", "").replace(")", "")
        embed = Embed(color = 16711680)
        embed.add_field(name=f'Trade request for {username_trade_request}',
                        value=f'{trade_requester.name}#{trade_requester.discriminator} wants to trade your username for:\n{note}')
        await self.client.get_user(seller_id).send(embed=embed)
        await self.client.get_user(seller_id).send(
            f"\nIf you accept do - !accept {username_trade_request}\nIf you want to decline the trade do - !decline {username_trade_request}")
        embed = Embed(color = 16711680)
        embed.add_field(name=f'Trade details sent',
                        value=f'Waiting for seller\'s response')
        await ctx.message.author.send(embed=embed)

        def check(m):
            return (
                           m.content == f'!accept {username_trade_request}' or m.content == f'!decline {username_trade_request}') and m.author.id == self.client.get_user(
                seller_id).id

        msg = await self.client.wait_for('message', check=check)
        if msg.content == f'!accept {username_trade_request}':
            await  self.client.get_user(trade_requester.id).send(
                f'The seller has accepted your offer, for - {username_trade_request}\nPlease check MJ Server')
            await self.client.get_user(seller_id).send('Please check MJ server')
            overwrites = {  # CREATES A PRIVATE CHANNEL IN GUILDS
                self.client.get_guild(788462475430461451).default_role: discord.PermissionOverwrite(
                    read_messages=False),
                await self.client.get_guild(788462475430461451).fetch_member(
                    int(trade_requester.id)): discord.PermissionOverwrite(read_messages=True),
                await self.client.get_guild(788462475430461451).fetch_member(
                    int(seller_id)): discord.PermissionOverwrite(read_messages=True)
            }
            cc = await self.client.get_guild(788462475430461451).create_text_channel('trade' + username_trade_request,
                                                                                     overwrites=overwrites)
            await self.client.get_channel(cc.id).send(self.client.get_guild(788462475430461451).default_role)


        elif msg.content == f'!decline {username_trade_request}':
            await  self.client.get_user(trade_requester.id).send(
                f'The seller has rejected your offer, for - {username_trade_request}')
        else:
            await self.client.get_channel(737997940085489684).send('There has been an error using !trade command')
        mj_market.close()

    @commands.command()
    @commands.has_role("Admin")
    async def deleteall(self, ctx):
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        cmj.execute("DELETE FROM mjmarket")
        mj_market.commit()
        mj_market.close()
        await ctx.message.add_reaction("✅")






    @commands.command()
    async def soldall(self, ctx):

        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        seller_id = ctx.author.id
        try:
            users = cmj.execute("SELECT username FROM mjmarket WHERE seller_name=:seller_name ",
                                {"seller_name": seller_id}).fetchall()
            print(users)
            for user in users:
                user = user[0]
                cmj.execute("DELETE FROM mjmarket WHERE username=:username", {"username": user})
                mj_market.commit()
                embed = Embed(color = 16711680)
                embed.add_field(name=f"**@{user}** has been sold! ",
                                value=f"Seller: @{ctx.author.name}#{ctx.author.discriminator}")
                await self.client.get_channel(746408135144505462).send(embed=embed)
                await ctx.message.add_reaction("✅")

        except Exception as e:
            print(e)


def setup(client):
    client.add_cog(Market(client))


