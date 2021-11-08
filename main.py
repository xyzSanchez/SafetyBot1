import discord
import os
import asyncio
from discord.ext.commands.cooldowns import BucketType
from discord.ext import commands
import json
from discord.utils import get

##------------------------------------------------------------------------------##
##------------------------------------------------------------------------------##
##---------------------------------INFORMATION----------------------------------##

TOKEN = "YOURTOKENHERE" # Get it from https://discord.com/developers/applications
STATUS = "YourBotStatusHere" # Change this to whatever you want the bot status to say.

PREFIX = "--"
# Bot developed by Oleyat @ https://www.fiverr.com/oleyat

##------------------------------------------------------------------------------##
##------------------------------------------------------------------------------##
##------------------------------------------------------------------------------##
intents = discord.Intents.default()
intents.members = True

activity = discord.Activity(type=discord.ActivityType.watching, name=STATUS)

bot = commands.Bot(command_prefix=PREFIX, activity=activity, status=discord.Status.online, intents=intents)
bot.remove_command("help")

extensions = [
  'Commands.blacklistauto' ,
]



@bot.event
async def on_ready():
  print("Online")

@bot.command()
@commands.has_permissions(administrator=True)
async def roleset(ctx, role: discord.Role):
  with open ('blacklist.json',  'r') as f:
    roleidthing = json.load(f)
  roleid = role.id
  if "badrole" not in roleidthing:
    roleidthing["badrole"] = roleid
  else:
    roleidthing["badrole"] = roleid  
  with open ('blacklist.json',  'w') as f:
    json.dump(roleidthing, f, indent=4)

@bot.command()
@commands.has_permissions(administrator=True)
async def logset(ctx, message):
  channelmentionextract = message.replace("<", "")
  channelmentionextract = channelmentionextract.replace(">", "")
  channelmentionextract = channelmentionextract.replace("#", "")
  print(channelmentionextract)
  cha = channelmentionextract
  with open ('blacklist.json',  'r') as f:
    roleidthing = json.load(f)
  if "logch" not in roleidthing:
    roleidthing["logch"] = cha
  else:
    roleidthing["logch"] = cha  
  with open ('blacklist.json',  'w') as f:
    json.dump(roleidthing, f, indent=4)

@bot.event
async def on_member_join(member):
  with open ('blacklist.json',  'r') as pf:
    blacklist = json.load(pf)
  if str(member.id) in blacklist:
    await member.ban(reason="AUTOBAN - User is in the blacklist database.")

@bot.event
async def on_member_update(before, after):
  with open ('blacklist.json',  'r') as f:
    roleidthing = json.load(f)
  guild = before.guild
  logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.member_role_update).flatten()
  try:
    badroles = int(roleidthing["badrole"])
  except:
    return
  badrole = get(after.guild.roles, id=badroles)
  if badrole in before.roles:
    print(len(before.roles))
    if len(after.roles) == 2:
      return
    await after.remove_roles(badrole)


@bot.event
async def on_member_ban(guild, member):
    with open ('modact.json',  'r') as f:
      memberuser = json.load(f)
    with open ('blacklist.json',  'r') as f:
      channelog = json.load(f)
    logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.ban).flatten()
    try:
      channel = guild.get_channel(int(channelog["logch"]))
    except:
      pass
    logs = logs[0]
    if logs.user.bot == True:
      return
    if logs.target == member:
      if str(logs.user.id) not in memberuser:
        memberuser[logs.user.id] = {"bans": 1, "channels" : 0}
        with open ('modact.json',  'w') as f:
          json.dump(memberuser, f, indent=4)
      else:
          memberuser[str(logs.user.id)]["bans"] += 1
          if memberuser[str(logs.user.id)]["bans"] == 4:
            await guild.ban(logs.user, reason="AUTOBAN - Kicked/Banned more than 3 people in a day.")
            try:
              await channel.send(f'**AUTOBAN** - {logs.user.mention} was banned for kicking/banning more than 3 people in a day')
            except:
              pass
          with open ('modact.json',  'w') as f:
            json.dump(memberuser, f, indent=4)


@bot.event
async def on_member_remove(member):
    with open ('modact.json',  'r') as f:
      memberuser = json.load(f)
    with open ('blacklist.json',  'r') as f:
      channelog = json.load(f)
    guild = member.guild
    logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.kick).flatten()
    try:
      channel = guild.get_channel(int(channelog["logch"]))
    except:
      pass
    logs = logs[0]
    if logs.user.bot == True:
      return
    if logs.target == member:
      if str(logs.user.id) not in memberuser:
        memberuser[str(logs.user.id)] = {"bans": 1, "channels" : 0}
        with open ('modact.json',  'w') as f:
          json.dump(memberuser, f, indent=4)
      else:
          memberuser[str(logs.user.id)]["bans"] += 1
          if memberuser[str(logs.user.id)]["bans"] == 4:
            await guild.ban(logs.user, reason="AUTOBAN - Kicked/Banned more than 3 people in a day.")
            try:
              await channel.send(f'**AUTOBAN** - {logs.user.mention} was banned for kicking/banning more than 3 people in a day')
            except:
              pass
          with open ('modact.json',  'w') as f:
            json.dump(memberuser, f, indent=4)

@bot.event
async def on_guild_channel_delete(channel):
    guild = channel.guild
    with open ('modact.json',  'r') as f:
      memberuser = json.load(f)
    with open ('blacklist.json',  'r') as f:
      channelog = json.load(f)
    logs = await channel.guild.audit_logs(action=discord.AuditLogAction.channel_delete, limit=1).get()
    try:
      channel = guild.get_channel(int(channelog["logch"]))
    except:
      pass
    #logs = logs[0]
    ok = True
    if ok == True:
      if str(logs.user.id) not in memberuser:
        memberuser[str(logs.user.id)] = {"bans": 0, "channels" : 1}
        with open ('modact.json',  'w') as f:
          json.dump(memberuser, f, indent=4)
      else:
          memberuser[str(logs.user.id)]["channels"] += 1
          if memberuser[str(logs.user.id)]["channels"] == 4:
            await guild.ban(logs.user, reason="AUTOBAN - Deleted more than 3 channels in a day.")
            try:
              await channel.send(f'**AUTOBAN** - {logs.user.mention} was banned for deleting more than 3 channels in a day.')
            except:
              pass
          with open ('modact.json',  'w') as f:
            json.dump(memberuser, f, indent=4)


if __name__ == "__main__":
  for extension in extensions:
    try:
      bot.load_extension(extension)
    except Exception as error:
      print('{} cannot be loaded. [{}]'.format(extension, error))

  bot.run(TOKEN)
