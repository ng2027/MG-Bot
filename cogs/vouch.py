import sqlite3, discord, re, random, asyncio
import sys

from discord.ext import commands
from dhooks import Embed
from random import choice
from random import randint
import time
from time import sleep
import traceback

#######################################################################TABLE STRUCTURE##########################################
# cmj.execute("""CREATE TABLE vouches(
#            seller_id TEXT(35) PRIMARY KEY,
#            vouch_number INTEGER DEFAULT 0)
#           """)
# cmj.execute("""CREATE TABLE vouchers(
#            member_id TEXT(35),
#           vouched_id TEXT(35)
#           PRIMARY KEY(member_id, vouched_id)
#            )
#            """)

# cmj.execute("CREATE TABLE dwc("
#             "scammed TEXT(35),"
#             "scammer TEXT(35),"
#             "PRIMARY KEY(scammed, scammer)"
#             ")")


# mj_market db access
# cmj cursor for mj_market

sentences = [
"MG BOT> EBAY",
"beep boop",
"-- --. / -... --- -"
]


class Vouch(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.list_of_confirms = []

    claimed = False

    @commands.command(pass_context=True,
                      description="Admin command -  use this command to decrease someone's vouches by 1.. Example: !dvouch @mj")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def dvouch(self, ctx, member: discord.Member):
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()

        cmj.execute("UPDATE vouches SET vouch_number = vouch_number-1 WHERE seller_id=:seller_id",
                    {"seller_id": member.id})
        mj_market.commit()
        await ctx.message.add_reaction("✅")
        mj_market.close()

    @commands.command(pass_context=True,
                      description="Admin command -  use this command to increase someone's vouches by 1.. Example: !avouch @mj")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)

    async def avouch(self, ctx, member: discord.Member, amount=None):
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        if amount:
            vouches_num = int(cmj.execute("SELECT vouch_number FROM vouches WHERE seller_id=:seller_id", {"seller_id": member.id}).fetchone()[0])
            print(vouches_num)

            vouches_num += int(amount)
            cmj.execute(f"UPDATE vouches SET vouch_number = :vouch_num WHERE seller_id=:seller_id",
                        {"vouch_num": vouches_num,"seller_id": member.id})
            mj_market.commit()
            await ctx.message.add_reaction("✅")
            return
        cmj.execute("UPDATE vouches SET vouch_number = vouch_number+1 WHERE seller_id=:seller_id",
                    {"seller_id": member.id})
        mj_market.commit()
        await ctx.message.add_reaction("✅")
        mj_market.close()
    @commands.command(pass_context=True,
                      description="Admin command -  use this command to reset someones vouches to 0. Example: !rvouch @ng")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def rvouch(self, ctx, member: discord.Member):
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        member_id = str(member.id)
        cmj.execute("DELETE FROM vouches WHERE seller_id=:seller_id", {"seller_id": member_id})
        mj_market.commit()
        cmj.execute("UPDATE dwc SET scammed=NULL, scammer=NULL WHERE scammer=:scammer OR scammed=:scammed",
                    {"scammer": member_id, "scammed": member_id})
        mj_market.commit()
        cmj.execute("DELETE FROM vouchers WHERE vouched_id=:vouched_id OR member_id=:member_id",
                    {"vouched_id": member.id, "member_id": member_id})
        mj_market.commit()
        await ctx.message.add_reaction("✅")
        mj_market.close()

    @commands.command(pass_context=True,
                      description="Admin command -  use this command to update the leaderboard in #vouches-leaderboard. Example of use: !leaderboard")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def leaderboard(self, ctx):
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        while_loop_break = False
        try:  # leaderboard for channel
            await self.client.get_channel(808001267632308224).purge(limit=1)
            vouches = cmj.execute(
                "SELECT vouches.seller_id, vouches.vouch_number FROM vouches ORDER BY vouch_number DESC").fetchmany(
                30)
            embed = Embed(color = 16711680)
            embed.set_title(title="**Top 21 most vouched members in this server:**")
            pages_sent = 1
            number_of_pages = len(vouches) // 24
            remainder = len(vouches) % 24
            loops = 0
            index = 0
            users_added = 0
            if remainder != 0:
                number_of_pages = number_of_pages + 1
            while pages_sent <= number_of_pages:
                loops += 1
                if loops == 1:
                    vouches = vouches[index:]
                else:
                    vouches = vouches[index + 1:]
                for seller in vouches:
                    seller_id = seller[0]
                    binprice = seller[1]
                    index = vouches.index(seller)
                    counter = index
                    try:
                        if counter + 1 <= 3:
                            embed.add_field(
                                name=f":trophy:@{self.client.get_user(int(seller_id)).name}#{self.client.get_user(int(seller_id)).discriminator}- {binprice} :trophy:   ",
                                value=f"---------",
                                inline=True)
                        else:
                            embed.add_field(
                                name=f"@{self.client.get_user(int(seller_id)).name}#{self.client.get_user(int(seller_id)).discriminator}- {binprice}",
                                value=f"---------",
                                inline=True)
                        users_added += 1

                    except:
                        continue
                    if users_added == 21:
                        while_loop_break = True
                        break

                    counter += 1
                    if counter > 24:
                        break

                await self.client.get_channel(808001267632308224).send(embed=embed)
                embed = Embed(color = 16711680)
                pages_sent += 1
                if while_loop_break:
                    break
        except Exception as e:
            print(e)
        mj_market.close()

    @commands.command(pass_context=True,
                      description="You can use this command to vouch a person Use this command only when you have dealt with someone in a deal of 20 USD or more!. Example: !voucb @ng")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def vouch(self, ctx, member_to_be_vouched: discord.Member):
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        global claimed
        try:
            voucher_id = str(ctx.message.author.id)
            result = cmj.execute("SELECT * FROM dwc WHERE scammed=:scammed AND scammer=:scammer",
                                 {"scammed": str(ctx.message.author.id),
                                  "scammer": str(member_to_be_vouched.id)}).fetchone()
            if result is not None:
                embed = Embed(color = 16711680)
                embed.add_field(name="NO!",
                                value="You cannot vouch a member after using the !dwc commannd on them!")
                await ctx.send(embed=embed)
                return
            time.sleep(0.5)
            vouched_before = cmj.execute(
                "SELECT * FROM vouchers WHERE member_id = :member_id and vouched_id = :vouched_id",
                {'member_id': voucher_id, 'vouched_id': str(member_to_be_vouched.id)}).fetchall()
            if str(vouched_before) == '[]':
                seller_in_table = cmj.execute("SELECT vouches.seller_id FROM vouches WHERE seller_id = :seller_id",
                                              {'seller_id': str(member_to_be_vouched.id)}).fetchall()
                if not seller_in_table:
                    cmj.execute("INSERT INTO vouches VALUES(:seller_id, 1)",
                                {'seller_id': str(member_to_be_vouched.id)})
                    mj_market.commit()
                    cmj.execute("INSERT INTO vouchers(member_id, vouched_id) VALUES (:member_id, :vouched_id)",
                                {"member_id": voucher_id, "vouched_id": str(member_to_be_vouched.id)})
                    mj_market.commit()
                else:
                    cmj.execute("UPDATE vouches SET vouch_number = vouch_number+1 WHERE seller_id = :seller",
                                {'seller': str(member_to_be_vouched.id)})
                    mj_market.commit()
                    vouch_number = cmj.execute("SELECT vouches.vouch_number FROM vouches WHERE seller_id=:seller_id ",
                                               {"seller_id": member_to_be_vouched.id}).fetchone()[0]
                    if vouch_number == 63:
                        await member_to_be_vouched.add_roles(
                            discord.utils.get(member_to_be_vouched.guild.roles, name="trusted"))
                    elif vouch_number == 126:
                        await member_to_be_vouched.add_roles(
                            discord.utils.get(member_to_be_vouched.guild.roles, name="super trusted"))
                    cmj.execute("INSERT INTO vouchers(member_id, vouched_id) VALUES (:member_id, :vouched_id)",
                                {"member_id": voucher_id, "vouched_id": str(member_to_be_vouched.id)})

                    mj_market.commit()
                await self.leaderboard(ctx)

                await ctx.message.add_reaction("✅")

            elif vouched_before is not None:
                embed = Embed(color = 16711680)
                embed.add_field(name="invite people to this server thanks",
                                value="You have already vouched this member.")
                await ctx.send(embed=embed)
                await ctx.message.add_reaction("✅")
            else:
                await ctx.send(
                    'There was an error executing the !vouch command. Please message an admin to resolve this issue.')
        except Exception as e:
            print(e)
            await ctx.send('There has been an error using the !vouch command. Please use in MJ server.')
        mj_market.close()

    @commands.command(pass_context=True, name="removevouch",
                      description="You can use this command to remove a vouch from people you're already vouching. Example: !removevouch @mj")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def removevouch(self, ctx, member_to_remove_vouch_from: discord.Member):
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        try:
            vouched_id = str(member_to_remove_vouch_from.id)
            user_id = str(ctx.message.author.id)

            vouched_alr = cmj.execute("SELECT * FROM vouchers WHERE member_id = :user_id AND vouched_id=:vouched_id",
                                      {"user_id": user_id, "vouched_id": vouched_id}).fetchone()
            if vouched_alr is None:
                embed = Embed(color = 16711680)
                embed.add_field(name="You have not vouched this member before.",
                                value="You can use this command to remove a vouch from people you're already vouching.")
                await ctx.send(embed=embed)

            else:
                cmj.execute("DELETE FROM vouchers WHERE member_id = :user_id AND vouched_id=:vouched_id ",
                            {"user_id": user_id, "vouched_id": vouched_id})
                mj_market.commit()
                cmj.execute("UPDATE vouches SET vouch_number = vouch_number - 1 WHERE seller_id=:seller_id",
                            {"seller_id": vouched_id})
                mj_market.commit()
            await ctx.message.add_reaction("✅")

        except Exception as e:
            print(e)
            await ctx.send('There was an error using the!removevouch command.')
        mj_market.close()

    @commands.command(pass_context=True, name="rep",
                      description="This command shows how many vouches a member in this server has. Example: !rep @ng")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def rep(self, ctx, member: discord.Member):
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        global claimed
        try:
            vouches = cmj.execute("SELECT vouches.vouch_number FROM vouches WHERE seller_id=:seller_id",
                                  {"seller_id": member.id}).fetchone()
            if vouches is None:
                embed = Embed(color = 16711680)
                embed.add_field(name=f"Vouches for {member.name}#{member.discriminator}:",
                                value="This member has no vouches.")
                await ctx.send(embed=embed)
            else:
                embed = Embed(color = 16711680)
                embed.add_field(name=f"Vouches for {member.name}#{member.discriminator}:",
                                value="This member has {} vouches.".format(str(vouches[0])))
                await ctx.send(embed=embed)
            await ctx.message.add_reaction("✅")
            


        except Exception as e:
            print(e)
            await ctx.send('There has been an error using the !rep command')
        mj_market.close()

    @commands.command(pass_context=True, name="confirm", description="Confirm your dwc command.")
    async def confirm(self, ctx):
        global list_of_confirms
        self.list_of_confirms.append(f"{str(ctx.author)}")
        await ctx.message.add_reaction("✅")

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(pass_context=True, name="dwc",
                      description="You can use this command to increase someone's dwc count by 1, and remove a vouch from them. Keep in mind that misuse will lead to consequences.")
    async def dwc(self, ctx, scammer_name: discord.Member):
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        global list_of_confirms
        print(self.list_of_confirms)
        try:
            scammed = str(ctx.message.author.id)
            scammer = str(scammer_name.id)
            ids = ["294104078668136449", "443398625624588299", "705810401530609695", "680080613780226068"]
            print(self.list_of_confirms)
            if str(ctx.author) not in self.list_of_confirms:
                embed = Embed(color = 16711680)
                embed.add_field(
                    name="Please make sure you have sufficient proof that this person has scammed you directly.",
                    value="Type !confirm if this person has scammed you. If you are misusing this, you will receive 3 warnings.")
                await ctx.send(embed=embed)
                return
            else:
                self.list_of_confirms.remove(str(ctx.author))

            if scammer not in ids:
                in_vouches = cmj.execute("SELECT * FROM vouches WHERE seller_id=:vouched_id",
                                         {"vouched_id": scammer}).fetchone()
                if in_vouches is None:
                    cmj.execute("INSERT INTO vouches VALUES(:vouched_id, 0)", {"vouched_id": scammer})
                    mj_market.commit()
                result = cmj.execute("SELECT * FROM vouchers WHERE member_id=:user_id AND vouched_id=:dwc_id",
                                     {"user_id": scammed, "dwc_id": scammer}).fetchone()
                if result is None:
                    cmj.execute("INSERT INTO dwc values(:scammed, :scammer)", {"scammed": scammed, "scammer": scammer})
                    mj_market.commit()
                    cmj.execute("UPDATE vouches SET vouch_number=vouch_number-1 WHERE seller_id=:scammer",
                                {"scammer": scammer})
                    mj_market.commit()
                    await ctx.message.add_reaction("✅")
                else:
                    embed = Embed(color = 16711680)
                    embed.add_field(name="Operation failed.",
                                    value="You are currently vouching this member. Please remove your vouch using !removevouch before trying to mark this person as a scammer.")
                    await ctx.send(embed=embed)
                dwc_count = cmj.execute("SELECT * FROM dwc WHERE scammer=:scammer", {"scammer": scammer}).fetchall()
                role = discord.utils.get(ctx.author.guild.roles, name="super trusted")
                role1 = discord.utils.get(ctx.author.guild.roles, name="trusted")
                role2 = discord.utils.get(ctx.author.guild.roles, name="dwc")
                roles = scammer_name.roles
                if len(dwc_count) == 4:

                    if role in roles:
                        await scammer_name.remove_roles(role, "received 2 dwc complaints from members in server")
                        await scammer_name.add_roles(role1, "received 2 dwc complaints from members in server")
                    elif role1 in roles:
                        await scammer_name.remove_roles(role1, "received 2 dwc complaints from members in server")
                    else:
                        await scammer_name.add_roles(role2)

            else:
                embed = Embed(color = 16711680)
                embed.add_field(
                    name=f"EE ERR EEE ERR",
                    value="You cannot mark an admin or a bot as a scammer!")
                await ctx.send(embed=embed)

            embed = Embed(color = 16711680)
            embed.add_field(name="DWC has been used.",
                            value=f"{str(ctx.author)} has used !dwc on {scammer_name.name}#{scammer_name.discriminator}")
            await self.client.get_channel(802686280450179113).send(embed=embed)
            await self.leaderboard(ctx)


        except Exception as e:
            if str(e) == 'UNIQUE constraint failed: dwc.scammed, dwc.scammer':
                embed = Embed(color = 16711680)
                embed.add_field(name=f'come on man *()*',
                                value='You already used !dwc on this person')
                await ctx.send(embed=embed)
                return
            print(e)
            await ctx.send('There has been an error using the !dwc command. Please use in NJ SERVER')
        mj_market.close()

    @commands.command(pass_context=True, name="removedwc",
                      description="You can use this command to remove dwc from people you've marked as a scammer. Example: !removedwc @nj")
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def removedwc(self, ctx, member_to_remove_dwc_from: discord.Member):
        mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
        cmj = mj_market.cursor()
        try:
            vouched_id = str(member_to_remove_dwc_from.id)
            user_id = str(ctx.author.id)

            vouched_alr = cmj.execute("SELECT * FROM dwc WHERE scammed = :user_id AND scammer=:vouched_id",
                                      {"user_id": user_id, "vouched_id": vouched_id}).fetchone()
            if vouched_alr is None:
                embed = Embed(color = 16711680)
                embed.add_field(name="You have not used !dwc on this member before.",
                                value="You can use this command to remove an existing dwc from a member.")
                await ctx.send(embed=embed)

            else:
                cmj.execute("DELETE FROM dwc WHERE scammed = :user_id AND scammer =:vouched_id ",
                            {"user_id": user_id, "vouched_id": vouched_id})
                mj_market.commit()
                cmj.execute("UPDATE vouches SET vouch_number = vouch_number + 1 WHERE seller_id=:seller_id",
                            {"seller_id": vouched_id})
                mj_market.commit()
                dwc_count = cmj.execute("SELECT * FROM dwc WHERE scammer=:scammer", {"scammer": user_id}).fetchall()
                role2 = discord.utils.get(ctx.author.guild.roles, name="scammer")
                if len(dwc_count) < 2:
                    await member_to_remove_dwc_from.remove_roles(role2)

            await ctx.message.add_reaction("✅")


        except Exception as e:
            print(e)
            embed = Embed(color = 16711680)
            embed.add_field(name="Error time",
                            value="Please contact an admin immediately and explain to them exactly what happened so they can fix this issue.")
            await ctx.send(embed=embed)
        mj_market.close()

    @commands.command(pass_context=True, description="""This command allows you to create a channel between you and another member. You, this member and moderators in this server will be able to sort any problems between you two, and an admin will make a final decision as to what happens to who.
To use: !dispute @mj""")
    async def dispute(self, ctx, *members: discord.Member):

        disputer = ctx.message.author.id
        overwrites = {  # CREATES A PRIVATE CHANNEL IN GUILDS
            self.client.get_guild(788462475430461451).default_role: discord.PermissionOverwrite(read_messages=False,
                                                                                                send_messages=True, view_channel = False),
            await self.client.get_guild(788462475430461451).fetch_member(int(disputer)): discord.PermissionOverwrite(
                read_messages=True, send_messages=True),
            self.client.get_guild(788462475430461451).get_role(int(802686091743330304)): discord.PermissionOverwrite(
                read_messages=True, send_messages=True)
        }
        cc = await self.client.get_guild(788462475430461451).create_text_channel('dispute-' + ctx.message.author.name,
                                                                                 overwrites=overwrites)  # CREATES CHANNEL AND PINGS PEOPLE
        for member in members:
            member = await self.client.get_guild(788462475430461451).fetch_member(member.id)
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = True
            await self.client.get_guild(788462475430461451).get_channel(int(cc.id)).set_permissions(member,
                                                                                                    read_messages=True,
                                                                                                    send_messages=True)
        await self.client.get_channel(int(cc.id)).send(self.client.get_guild(788462475430461451).default_role)

    @commands.command()
    async def vouches(self, ctx, member: discord.Member):
        try:
            mj_market = sqlite3.connect("mj_discord_market.db", timeout=5)
            cmj = mj_market.cursor()
            seller_id = str(member.id)

            vouches = cmj.execute("SELECT member_id FROM vouchers WHERE vouched_id=:seller_id",
                                  {"seller_id": seller_id}).fetchall()
            embed = Embed(color = 16711680)
            embed.add_field(
                name=f"{self.client.get_user(member.id).name}#{self.client.get_user(member.id).discriminator}'s vouchers are:",
                value="----------------------------", inline=False)
            counter = 0
            index = 0
            for vouch in vouches:
                vouch = vouch[0]
                counter += 1
                index += 1

                try:

                    embed.add_field(
                        name=f"{str(counter)}.", value =F"{self.client.get_user(int(vouch)).name}#{self.client.get_user(int(vouch)).discriminator}")
                except:
                    pass
                if index >= 24:
                    await ctx.send(embed=embed)
                    embed = Embed(color = 16711680)
                    index = 0
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)
            await ctx.send(
                "It looks like there was an error using the !vouches command. Message an admin and explain to them what happened so this can get fixed as soon as possible.")


def setup(client):
    client.add_cog(Vouch(client))

