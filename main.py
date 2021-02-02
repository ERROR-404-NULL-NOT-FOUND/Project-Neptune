import discord
import random
import datetime
'''
import youtube_dl
import os
'''
from discord.ext import commands

intents = discord.Intents.all()
intents.members = True
token_file = open("token.tk")
token = token_file.read()
prefix = ['ERROR ', 'error ']
client = commands.Bot(command_prefix=prefix, intents=intents)
client.remove_command('help')
openChannel = 0


@client.event
async def on_command_error(ctx, error):
    print(error)
    await ctx.send(error)


@client.event
async def on_ready():
    print('Bot is ready')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                           name="Req make poor choices"))


@client.command()
async def remove_reactions(ctx, message):
    message = await ctx.channel.fetch_message(message)
    for r in message.reactions:
        await message.clear_reaction(r)


@client.command(description="Returns pong, then bot edits the message to include the client latency")
async def ping(ctx):
    embed = discord.Embed(title="Pong!")
    message = await ctx.send(embed=embed)
    embed.description = f'{int(client.latency*1000)} Milliseconds'
    await message.edit(embed=embed)


@client.command(description="Verifies a user, giving them the lowest role in the server")
async def verify(ctx):
    random.seed(ctx.author.id)
    characters = 'abcdefghijklmnopqrstuvwxyz _/?=,\\.[]{}-_=+;:\'"><'
    code = ''
    for i in range(20):
        code += str(characters[random.randint(0, len(characters)-1)])
    embed = discord.Embed(title="User verification for"+ctx.guild.name, description="""Please send the following code to verify that you are not a bot:\n
     `"""+code+"`")
    await ctx.send(embed=embed)
    response = await client.wait_for('message')
    while response.author != ctx.author:
        response = await client.wait_for('message')
    if response.content == code:
        await ctx.author.add_roles(ctx.guild.roles[1])
        await ctx.send("Verified!")
    else:
        await ctx.send("You have failed the captcha, you are now slightly more bot")


'''client.command()
async def destroy_server(ctx):
    channel=await ctx.guild.get_channel("General")

'''


@client.command(description="Prints almost all guild data available to the bot")
async def guild_info(ctx):
    embed = discord.Embed(title=f'Stats for {ctx.guild.name}')
    embed.set_thumbnail(url=ctx.guild.icon_url)
    owner = ctx.guild.owner
    embed.add_field(name='Owner', value=owner.mention, inline=True)
    embed.add_field(name='Number of members', value=str(ctx.guild.member_count), inline=True)
    embed.add_field(name='Guild created', value=str(ctx.guild.created_at)[:11], inline=True)
    embed.add_field(name='Number of roles', value=str(len(ctx.guild.roles)), inline=True)
    embed.add_field(name='Number of text channels', value=str(len(ctx.guild.text_channels)), inline=True)
    embed.add_field(name='Number of voice channels', value=str(len(ctx.guild.voice_channels)), inline=True)
    embed.add_field(name='Boosts', value=str(ctx.guild.premium_subscription_count), inline=True)
    embed.add_field(name='Server region', value=ctx.guild.region, inline=True)
    embed.set_footer(text=str(ctx.author) + ' at ' + str(datetime.datetime.now())[:16], icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@client.command(description="Creates a role with the specified name, color, and perms")
async def create_role(ctx, name, color: discord.Color):
    name = await ctx.guild.create_role(name=name, color=color, mentionable=True)
    await ctx.send(f'The role {name.mention} has been created')


@client.command(description="Deletes the specified role")
async def delete_role(ctx, role_name: discord.Role):
    await ctx.guild.delete_role(role_name)
    await ctx.send(f'The role {role_name} has been deleted')


@client.command(description="Bans the specified user from the guild")
@commands.has_guild_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, reason1=None):
    print("ban command activated")
    if not member.id == 716469153812447233:
        print("banning user"+member.display_name)
        await ctx.guild.ban(member, reason=reason1)
        print(member.display_name+"BANNED")
        await ctx.send("User "+str(member)+" banned!")
    else:
        await ctx.send("Nope. Not banning ERROR")


@client.command(description="Locks the specified channel")
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)


@client.command(description="Unlocks the specified channel")
async def unlock(ctx, channel: discord.TextChannel):
    embed = discord.Embed(title="UNLOCKED!", color=ctx.author.color)
    await channel.send(embed=embed)
    await channel.set_permissions(ctx.guild.default_role, send_messages=True)


@client.command(description="Kicks the specified user from the guild")
async def kick(ctx, member: discord.Member, reason=None):
    await ctx.guild.kick(member, reason=reason)
    await ctx.send("Kicked "+str(member)+"!")


@client.command(description="Saves the above message(warning: saves the message executing the command instead)")
async def archive(ctx):
    archived = open("archived.txt", 'a')
    message_to_archive = ctx.channel.history(limit=1).flatten
    archived.write(f'\n{message_to_archive}\n')
    await ctx.send("Archived message: `"+message_to_archive+'`!')
    archived.close()


@client.command(description="Lowers all letters in the message to the lowers")
async def to_lower(ctx, message):
    await ctx.send(message.lower())


@client.command(description="Raises all letters in the message to the uppercase")
async def to_upper(ctx, message):
    await ctx.send(message.upper())


@client.command(description="Shows the list of archives(warning: archives are not currently working)")
async def archive_list(ctx):
    archived = open("archived.txt", "r")
    embed = discord.Embed(title="Archived messages", description=str(archived.read()))
    await ctx.send(embed=embed)


@client.command(description="Lists almost all of the attributes of that user available to the bot")
async def user(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    embed = discord.Embed(title=member.name, color=member.color)
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="User created", value=f'`{str(member.created_at)[:10]}`')
    embed.add_field(name='Username VS nickname', value=f'Nickname: **{member.nick}**\nUsername: **{member.name}**')
    embed.add_field(name='Bot', value=member.bot, inline=True)
    embed.add_field(name='Joined server', value=f'`{str(member.joined_at)[:10]}`', inline=True)
    message = ''
    if str(member.raw_status) == 'online':
        message = "<:status_online:802704115746209854>"
    elif str(member.raw_status) == 'offline':
        message = "<:status_offline:802704116191199302>"
    elif str(member.raw_status) == 'dnd':
        message = "<:status_dnd:802704115699417160>"
    elif str(member.raw_status) == 'idle':
        message = "<:status_idle:802704115813187607>"
    embed.add_field(name='Status', value=f'{message} **{member.raw_status}**', inline=True)
    embed.add_field(name='Custom status', value=member.activity)
    if member.is_on_mobile():
        message = "User is on mobile"
    else:
        message = "User is on Desktop"
    embed.add_field(name='Discord Client', value=message, inline=True)
    message = ''
    for i in range(len(member.roles)):
        if not i == 0:
            message += f'<@&{member.roles[i].id}>\n'
    embed.add_field(name='Roles', value=message, inline=True)
    embed.set_footer(text=str(ctx.author)+' at '+str(datetime.datetime.now())[:16], icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@client.command(description="Lists all of the servers the bot is in")
async def list_servers(ctx):
    message = ''
    if ctx.author.id == 716469153812447233:
        for i in range(len(client.guilds)):
            message += str(client.guilds[i]) + "\n"
        embed = discord.Embed(title="Servers that Project Neptune is in", description="Guilds: "+str(client.guilds))
        embed.add_field(name='Guilds', value=message, inline=False)
        await ctx.send(embed=embed)


@client.command(description="Deletes specified amount of messages")
@commands.has_guild_permissions(manage_messages=True)
async def clear(ctx, amount):

    await ctx.channel.purge(limit=int(amount+1))

'''
@client.command(description="Disconnects the bot from the channel to which it is currently connected")
async def leave(ctx):
    voice = ctx.voice_client
    await voice.disconnect()


@client.command(description="Plays the specified(youtube) link in the vc that the author is currently in")
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    name_of_channel = ctx.author.voice.channel
    if name_of_channel is not None:
        await name_of_channel.connect()
    else:
        await ctx.send("You are not currently connected to a voice channel!")
        return
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    embed = discord.Embed(title="Downloading song...")
    await ctx.send(embed=embed)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    embed = discord.Embed(title="Finished downloading!")
    await ctx.send(embed=embed)
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio(source="song.mp3"))
'''

@client.command(pass_context=True, description="Displays this message")
async def help(ctx):
    embed = discord.Embed(color=discord.Colour.red())
    embed.set_author(name="Help")
    for i in client.commands:
        embed.add_field(name=i.name, value='```'+str(i.description)+'.```', inline=True)
    await ctx.send(embed=embed)


@client.command(description="Pauses the music the bot is currently playing")
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("No audio is playing!")


@client.command(description="Resumes the music that the bot was playing before the 'pause' command was executed")
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("Audio is not paused!")


@client.command(description="Stops the music")
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


@client.command(description="Mutes the specified(Warning: does not work)")
async def mute(ctx, member: discord.Member = None, *, reason=None):
    author_perms = ctx.author.permissions_in(ctx.channel)
    if author_perms.manage_roles:
        if member is None:
            await ctx.send("Please specify who you want to mute!")
        else:
            embed = discord.Embed(
                title=f'{member} has been muted',
                description=f'{member.mention} has been muted',
                colour=discord.Colour.blurple()
            )
            embed.add_field(name='Reason :', value=f'{reason}', inline=True)
            embed.set_thumbnail(url='')   # u can put a thumbnail if u want

            embed.add_field(name='Muted by :', value=f'{ctx.author.mention}')
            await ctx.send(embed=embed)
            role = discord.utils.get(ctx.guild.roles, name='Muted')
            await member.add_roles(role)
            role1 = discord.utils.get(ctx.guild.roles, name=ctx.guild.roles[1])
            await member.remove_roles(role1)
    else:
        if author_perms.manage_roles:
            pass
        else:
            await ctx.message.delete()
            await ctx.send(f"**{ctx.author.mention} you don't have the permissions to do that!**")


@client.command(description="Lists the guild's roles")
async def list_roles(ctx):
    message = ''
    for i in range(len(ctx.guild.roles)):
        if i != 0:
            role = ctx.guild.roles[i]
            message += f'<@&{role.id}>\n '
    embed = discord.Embed(description=message)
    await ctx.send(embed=embed)


@client.command(description="Lists the guild's users")
async def list_users(ctx):
    message = ''
    owner = f'Owner: {ctx.guild.owner}'
    for i in range(len(ctx.guild.members)):
        user = ctx.guild.members[i]
        message += f'{user.mention}\n '
    embed = discord.Embed(title=f'Users for {ctx.guild.name}', description=message)
    embed.add_field(name=owner, value=f'Owner of {ctx.guild.name}', inline=False)
    await ctx.send(embed=embed)


@client.command(description="Creates an embed with a message prompt(Warning: does not work)")
async def embed_long(ctx):
    embed = discord.Embed()
    await ctx.send('what do you want the title to be?')
    title = await client.wait_for('message')
    embed.title = title.content
    await ctx.send('what do you want the description to be?')
    desc = await client.wait_for('message')
    embed.description = desc.content

    await ctx.send("what do you want the color to be?[int value]")
    color = await client.wait_for('message')
    embed.colour = int(color.content)

    await ctx.send("do you want to create a field?")
    input1 = await client.wait_for('message')
    create_field = str(input1.content).lower() == 'yes'
    while create_field:

        await ctx.send('what do you want the name to be?')
        name = await client.wait_for('message')

        await ctx.send("Do you want the text to be inline? [true or false]")
        inline = await client.wait_for('message')

        await ctx.send("what do you want the value to be")
        value = await client.wait_for('message')

        embed.add_field(name=name.content, inline=inline.content, value=value.content)
        await ctx.send("do you want to create a field?")
        input1 = await client.wait_for('message')
        create_field = str(input1.content).lower() == 'yes'
    await ctx.send(embed=embed)


@client.command(description="Creates and sends an embed with a title and description specified by the user")
async def embed_short(ctx):
    info = str(ctx.message.content)[17:].split("|")
    desc = info[1]
    title = info[0]
    embed = discord.Embed(description=desc, title=title, color=ctx.author.color)
    msg = await ctx.channel.fetch_message(ctx.message.id)
    await msg.delete()
    await ctx.send(embed=embed)


@client.event
async def on_message(message):

    if message.author == client.user:
        return
    log_channel = client.get_channel(795468867794763780)
    '''global channelLast
    lastChannel = channelLast
    lastChannel = client.get_channel(lastChannel)
    if message.channel == logChannel:
        await lastChannel.send(message.content)
        return'''

    author = message.author.name
    content = message.content
    channel = message.channel
    color = message.author.color
    desc = f'From: <@!{message.author.id}>'
    server = str(message.guild.name)
    if not message.guild:
        server = ''
        embed = discord.Embed(title=f'{message.content[19:]}', description=desc, color=color)
        await client.get_channel(int(message.content[:19])).send(embed=embed)

    print(f'''
    Server: {server}
        Channel: {channel}
            Author: {author}
                Message: {content}
''')

    embed = discord.Embed(description="", title=f'{message.content}', color=message.author.color)
    embed.add_field(name=author, value=f'{channel}, {server}', inline=True)
    embed.set_thumbnail(url=message.author.avatar_url)
    await log_channel.send(embed=embed)
    '''channelLast = int(message.channel)'''
    
    await client.process_commands(message)
client.run(token)
