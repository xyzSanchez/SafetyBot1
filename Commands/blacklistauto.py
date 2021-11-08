import discord
from discord.ext import commands, tasks
from discord.utils import get
import asyncio
from discord.ext.commands import command, Cog
import json


class blacklistauto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.dailycheck.start()
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    @tasks.loop(hours=24)
    async def dailycheck(self):
      with open ('modact.json',  'r') as f:
        memberuser = json.load(f)
      for users in memberuser:
        memberuser[users] = {"bans": 0, "channels" : 0}
        with open ('modact.json',  'w') as f:
          json.dump(memberuser, f, indent=4)
        

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def blacklist(self, ctx, id=None):
      if not id or id == None:
        await ctx.send("Missing id.")
        return
      with open ('blacklist.json',  'r') as f:
        blacklist = json.load(f)
      try:
        id = int(id)
      except:
        await ctx.send("ID must be a number.")
        return

      if str(id) in blacklist:
        blacklist.pop(str(id))
        await ctx.send("User was unblacklisted.")
      else:
        blacklist[str(id)] = "blacklisted"
        await ctx.send("User was blacklisted.")
      with open ('blacklist.json',  'w') as f:
        json.dump(blacklist, f, indent=4)

def setup(bot):
    bot.add_cog(blacklistauto(bot))


