# Import Discord Package
import discord
import time
import random
from discord.ext import commands, tasks
import datetime
import os
import discord.utils

# Client (bot)
client = commands.Bot(command_prefix='cs ')

#region DEL COMMAND
@client.command(name='del')
#@commands.has_permissions(manage_messages=True)
@commands.has_any_role('OWNER','Magenta')
async def dele(context, amount=5):
    try:
        await context.channel.purge(limit=amount+1)
        time.sleep(0.5)
        await context.message.channel.send('Deleted ' + str(amount) + ' messages.')
    except:
        await context.message.channel.send('No permissions.')
#endregion


#

#region USERINFO COMMAND
@client.command(name='userinfo')
async def userinfo(context, member: discord.Member):
    
    userinfoEmbed = discord.Embed(color = member.color, timestamp = context.message.created_at)
    userinfoEmbed.set_author(name = f'User Info - {member}')
    userinfoEmbed.set_thumbnail(url = member.avatar_url)
    userinfoEmbed.set_footer(text = f'Requested by: {context.author}', icon_url = context.author.avatar_url)

    userinfoEmbed.add_field(name = 'ID', value = member.id)
    userinfoEmbed.add_field(name = 'Server Nickname:', value = member.display_name)
    userinfoEmbed.add_field(name = 'Creation Date:', value = member.created_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
    userinfoEmbed.add_field(name = 'Joined at:', value = member.joined_at.strftime('%a, %#d %B %Y, %I:%M %p UTC'))
    userinfoEmbed.add_field(name = 'Highest Role:', value = member.top_role.mention)
    userinfoEmbed.add_field(name = 'Bot?', value = member.bot)
    #userinfoEmbed.add_field(name = 'Status:', value = member.status)


    await context.message.channel.send(embed=userinfoEmbed)
#endregion

#region SAY COMMAND
@client.command(name='say')
async def say(ctx, *, arg):
    try:
        await ctx.message.delete()
        await ctx.send(arg)
    except:
        await ctx.message.channel.send('sorry :/ i don\'t have permission to read messages...')
#endregion

#region DM COMMAND
@client.command(name='dm')
#@commands.has_permissions(manage_messages=True)
async def dm(context, member : discord.Member, *, arg):
    try:
        #sends arg to specified member
        await member.send(arg)

        #shows embed of who sent what to whom
        dmEmbed = discord.Embed(color = member.color, timestamp = context.message.created_at)
        dmEmbed.add_field(name = f'User: {member}', value = f'Message sent: {arg}')
        dmEmbed.set_thumbnail(url = member.avatar_url)
        dmEmbed.set_footer(text = f'Authorized by: {context.author}', icon_url = context.author.avatar_url)

        await context.message.channel.send(embed=dmEmbed)
    except:
        await context.message.channel.send('No permissions.')


#endregion



#region SNIPE COMMAND
@client.event
async def on_message_delete(message):

    #stores deleted message in a variable
    global deletedMessage
    deletedMessage = str(message.content)

    global deletedMessageUser
    deletedMessageUser = str(message.author)

    global deletedMessageChannel
    deletedMessageChannel = str(message.channel)

    now = datetime.datetime.now()
    timeitisnow = now.strftime('%I:%M %p')

    msg = str(message.author)+ ' deleted message in '+str(message.channel)+': '+str(message.content) + ' at ' + timeitisnow
    print(msg)

    deletedMessageLogs = client.get_channel(811964109309476894)
    await deletedMessageLogs.send(msg)

@client.command(name = 'snipe')
async def snipe(context):
    # msg = deletedMessageUser + ' deleted message in '+ deletedMessageChannel + ': ' + deletedMessage
    # await context.message.channel.send(msg)
    try:
        # snipeEmbed = discord.Embed(title = f'{deletedMessageUser} deleted message:', description = f'`{deletedMessage}`\n\n in #{deletedMessageChannel}',color=0x3E7FD3)
        # snipeEmbed.set_footer(text = f'Authorized by: {context.author} at {timeitisnow}', icon_url = context.author.avatar_url)
    
        # await context.message.channel.send(embed=snipeEmbed)
        
        msg = deletedMessageUser + ' deleted message in '+ deletedMessageChannel + ': ' + deletedMessage
        await context.message.channel.send(msg)

    except:
        await context.message.channel.send("No deleted message found!")




#endregion

# client.event

#region bot start-up message
@client.event
async def on_ready(message): #when bot starts up
    startup_channel = client.get_channel(799071963485831168)
    await startup_channel.send('CS Bot has come online')
    
    uwubotGeneral_channel = client.get_channel(794466074305232920)
    
    await client.change_presence(activity=discord.Activity(type = discord.ActivityType.listening, name = 'your commands!'))

#endregion






# Run the client on the server
client.run('ODk3MTk3MDIwMzEyMzc1MzA4.YWSJ1g.CYd8cXPQZuI13wsLfxbW0zvDKc4')