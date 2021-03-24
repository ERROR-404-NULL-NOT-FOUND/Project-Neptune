import discord
import random
import datetime
import json
import time

import os
import discord
import traceback
import inspect
import textwrap
import io

from discord.ext import commands
from contextlib import redirect_stdout
os.chdir(r'C:\Users\gigga.PAIGE\PycharmProjects\pythonProject\assets')

intents = discord.Intents.all()
intents.members = True
from discord.ext import commands
from discord_slash import SlashCommand
tokenFile = open('token.tk', 'r')
token = tokenFile.read()
prefix = ['ERROR ', 'error ']
client = commands.Bot(command_prefix=prefix, intents=intents)
slash = SlashCommand(client, sync_commands=True)
client.remove_command('help')
openChannel = 0
guild_ids = [739204995433496656, 771497539748233257, 729649553648910398, 788789142343122945, 729184659002490910]
print(guild_ids)


@client.event
async def on_command_error(ctx, error):
    print(error)
    await ctx.send(error)


'''client.event
async def on_voice_state_update(member, before, after):
    print(f'{member} has joined the vc~!')
    with open('usersVC.json','r') as f:
            users = json.load(f)
            if  not await search(users, member.display_name+member.discriminator):
                users[str(member.display_name+member.discriminator)] = {}
                users[str(member.display_name+member.discriminator)]['exp'] = 0
                users[str(member.display_name+member.discriminator)]['level'] = 1
                with open('usersVC.json', 'w') as w:
                    json.dump(users, w)
            while member.voice != None:
                await add_exp(users, member, 5)
                with open('usersVC.json', 'w') as w:
                    json.dump(users, w)
                time.sleep(60)
    print(f'{member} left the vc!')'''

@client.command(name="eval")  # Borrowed eval command. -R.Danny
async def _eval(ctx, *, body):
    if ctx.author.id == 716469153812447233:
        env = {
            "ctx": ctx,
            "bot": client,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "source": inspect.getsource,
        }

        def cleanup_code(content):
            """Automatically removes code blocks from the code."""
            # remove ```py\n```
            if content.startswith("```") and content.endswith("```"):
                return "\n".join(content.split("\n")[1:-1])

            # remove `foo`
            return content.strip("` \n")

        def get_syntax_error(e):
            if e.text is None:
                return f"```py\n{e.__class__.__name__}: {e}\n```"
            return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

        env.update(globals())

        body = cleanup_code(body)
        stdout = io.StringIO()
        err = out = None

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        def paginate(text: str):
            """Simple generator that paginates text."""
            last = 0
            pages = []
            for curr in range(0, len(text)):
                if curr % 1980 == 0:
                    pages.append(text[last:curr])
                    last = curr
                    appd_index = curr
            if appd_index != len(text) - 1:
                pages.append(text[last:curr])
            return list(filter(lambda a: a != "", pages))

        try:
            exec(to_compile, env)
        except Exception as e:
            err = await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")
            return await ctx.message.add_reaction("\u2049")

        func = env["func"]
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            err = await ctx.send(f"```py\n{value}{traceback.format_exc()}\n```")
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    try:

                        out = await ctx.send(f"```py\n{value}\n```")
                    except:
                        paginated_text = paginate(value)
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                out = await ctx.send(f"```py\n{page}\n```")
                                break
                            await ctx.send(f"```py\n{page}\n```")
            else:
                try:
                    out = await ctx.send(f"```py\n{value}{ret}\n```")
                except:
                    paginated_text = paginate(f"{value}{ret}")
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f"```py\n{page}\n```")
                            break
                        await ctx.send(f"```py\n{page}\n```")

        if out:
            await ctx.message.add_reaction("\u2705")  # tick
        elif err:
            await ctx.message.add_reaction("\u2049")  # x
        else:
            await ctx.message.add_reaction("\u2705")



@client.event
async def on_member_join(member):
    path = r"C:\Users\gigga.PAIGE\PycharmProjects\pythonProject\assets"
    os.chdir(r'C:\Users\gigga.PAIGE\PycharmProjects\pythonProject\assets')
    founddir = False
    if str(member.guild.id) in os.listdir(path):
        os.chdir(r'C:\Users\gigga.PAIGE\PycharmProjects\pythonProject\assets\{}'.format(member.guild.id))
        founddir = True
    if not founddir:
        os.mkdir(str(member.guild.id))
        os.chdir(r'C:\Users\gigga.PAIGE\PycharmProjects\pythonProject\assets\{}'.format(member.guild.id))
        open("usersText.json", "w+")
        f = open("usersText.json", "w")
        f.write('{}')
        f.close()
        open("levelallowed.txt", "w+")
        f = open("usersText.json", "w")
        f.write('True')
        f.close()
    with open('usersText.json', 'r') as f:
        users = json.load(f)
        await update_data(users, member)
    with open('usersText.json','w') as f:
        json.dump(users, f)


@client.event
async def on_ready():
    print('Bot is ready')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing,
                                                           name="Made by ERROR"))


@client.command()
async def remove_reactions(ctx, message):
    message = await ctx.channel.fetch_message(message)
    for r in message.reactions:
        await message.clear_reaction(r)


@slash.slash(guild_ids=guild_ids)
async def ttt(ctx):
    emojis = {"checkmark": '<:checkmark:821783910270369842>', "plusign": "<:plussign:821783451412987964>"}
    embed = discord.Embed(title=f'{ctx.author}\'s game of tic-tac-toe!', description=f'React with {emojis["plusign"]} to join!')
    embed.add_field(name="1/2 members!",value="Current members: "+ctx.author.display_name)
    message = await ctx.send(embed=embed)
    await message.add_reaction(emojis['plusign'])
    await message.add_reaction(emojis['checkmark'])
    emoji, member = await client.wait_for('reaction_add')
    while emoji.emoji.name != 'PlusSign' and member != client.user:
        emoji, member = await client.wait_for('reaction_add')
    await ctx.send(member.display_name)
    embed.clear_fields()
    embed2 = embed
    embed2.add_field(name="2/2 members!",value="Current members: "+ctx.author.display_name+','+member.display_name)
    embed2.description=f'{ctx.author.mention} react with {emojis["checkmark"]} to start the game!'
    await message.edit(embed=None)


@client.command(description="Returns the level of the given user(if none then it defaults to whoever sends the command")
async def level(ctx, member: discord.Member = None):
    if open("levelallowed.txt",'r').read == "False":
        return
    if member is None:
        member = ctx.author
    with open('usersText.json', 'r') as f:
        users = json.load(f)
        percent = str(users[str(member.id)]["exp"] ** (1 / 4)).split('.')
        visual = ''
        percent = percent[1]
        acPercent = percent[0]+percent[1]
        percent = percent[0]
        print(percent)
        for i in range(int(percent)):
            visual += '■'
        for i in range(10-int(percent)):
            visual+='□'
        embed = discord.Embed(title=f'Data for {member.display_name}', description=visual+' '+acPercent+'%', color=member.color)
        embed.add_field(name='EXP', value=str(users[str(member.id)]["exp"]), inline=True)
        embed.add_field(name='Level', value=str(users[str(member.id)]["level"]), inline=True)
        await ctx.send(embed=embed)



@client.command()
async def leaderboard(ctx):
    with open('levelAllowed.json', 'r') as f:
        guilds = json.load(f)
        if guilds[str(ctx.guild.id)]["allowed"] == False:
            return
    with open('usersText.json', 'r') as f:
        users = json.load(f)
        leaderboard = {key: val for key, val in sorted(users.items(), key = lambda ele: ele[1])}
        await ctx.send(leaderboard)



@client.command()
@commands.has_guild_permissions(manage_messages=True)
async def toggleTextLevel(ctx, onoroff: bool):
    onoroff = bool(onoroff)
    with open('levelAllowed.json', 'r') as f:
        guilds = json.load(f)
    guilds[str(ctx.guild.id)]['allowed'] = onoroff
    with open('levelAllowed.json', 'w') as f:
        json.dump(guilds,f)



@client.command(description="Returns pong, then bot edits the message to include the client latency")
async def ping(ctx):
    embed = discord.Embed(title="Pong!")
    message = await ctx.send(embed=embed)
    embed.description = f'{int(client.latency * 1000)} Milliseconds'
    await message.edit(embed=embed)


@client.command(description="Verifies a user, giving them the lowest role in the server")
async def verify(ctx):
    random.seed(ctx.author.id)
    characters = 'abcdefghijklmnopqrstuvwxyz _/?=,\\.[]{}-_=+;:\'"><'
    code = ''
    for i in range(20):
        code += str(characters[random.randint(0, len(characters) - 1)])
    embed = discord.Embed(title="User verification for" + ctx.guild.name, description="""Please send the following code to verify that you are not a bot:\n
     `""" + code + "`")
    embed.set_footer(text=str(ctx.author) + ' at ' + str(datetime.datetime.now())[:16], icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)
    response = await client.wait_for('message')
    while response.author != ctx.author:
        response = await client.wait_for('message')
    if response.content == code:
        await ctx.author.add_roles(ctx.guild.roles[1])
        await ctx.send("Verified!")
    else:
        await ctx.send("You have failed the captcha, you are now slightly more bot")


@slash.slash(name='guildInfo', guild_ids=guild_ids)
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
@commands.has_guild_permissions(manage_roles=True)
async def create_role(ctx, name, color: discord.Color):
    name = await ctx.guild.create_role(name=name, color=color, mentionable=True)
    await ctx.send(f'The role {name.mention} has been created')


@client.command(description="Deletes the specified role")
@commands.has_guild_permissions(manage_roles=True)
async def delete_role(ctx, role_name: discord.Role):
    await ctx.guild.delete_role(role_name)
    await ctx.send(f'The role {role_name} has been deleted')


@client.command(description="Bans the specified user from the guild")
@commands.has_guild_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, reason1=None):
    print("ban command activated")
    if not member.id == 716469153812447233:
        print("banning user" + member.display_name)
        await ctx.guild.ban(member, reason=reason1)
        print(member.display_name + " BANNED")
        await ctx.send("User " + str(member) + " banned!")
    else:
        await ctx.send("Nope. Not banning ERROR")


@client.command(description="Locks the specified channel")
@commands.has_guild_permissions(manage_messages=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)


@client.command(description="Unlocks the specified channel")
@commands.has_guild_permissions(manage_messages=True)
async def unlock(ctx, channel: discord.TextChannel):
    embed = discord.Embed(title="UNLOCKED!", color=ctx.author.color)
    await channel.send(embed=embed)
    await channel.set_permissions(ctx.guild.default_role, send_messages=True)


@client.command(description="Kicks the specified user from the guild")
@commands.has_guild_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, reason=None):
    await ctx.guild.kick(member, reason=reason)
    await ctx.send("Kicked " + str(member) + "!")



@slash.slash(name="user", guild_ids=guild_ids)
async def _user(ctx, member: discord.Member = None):
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
    embed.set_footer(text=str(ctx.author) + ' at ' + str(datetime.datetime.now())[:16], icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)


@client.command(desc="for ERROR only", hidden=True)
async def disable_all(ctx):
    if ctx.author.id == 716469153812447233:
        exit(0)


@client.command(description="Lists all of the servers the bot is in")
async def list_servers(ctx):
    message = ''
    if ctx.author.id == 716469153812447233:
        for i in range(len(client.guilds)):
            message += str(client.guilds[i]) + "\n"
        embed = discord.Embed(title="Servers that Project Neptune is in", description="Guilds: " + str(client.guilds))
        embed.add_field(name='Guilds', value=message, inline=False)
        await ctx.send(embed=embed)


@client.command(description="Deletes specified amount of messages")
@commands.has_guild_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=int(amount + 1))


@client.command(pass_context=True, description="Displays this message")
async def help(ctx):
    embed = discord.Embed(color=discord.Colour.red())
    embed.set_author(name="Help")
    for i in client.commands:
        embed.add_field(name=i.name, value='```' + str(i.description) + '.```', inline=True)
    await ctx.send(embed=embed)


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
            embed.set_thumbnail(url='')  # u can put a thumbnail if u want

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


@slash.slash(name="embedlong", guild_ids=guild_ids, description="Creates an embed with a message prompt(Warning: does not work)")
async def _embedlong(ctx, title, desc=None, color=None, fieldName=None, fieldValue=None, fieldInline=True):
    embed = discord.Embed(title=title, description=desc, color=int(color))
    embed.add_field(name=fieldName, value=fieldValue, inline=bool(fieldInline))
    await ctx.send(embed=embed)


@slash.slash(name='embedshort', guild_ids=guild_ids,description="Creates and sends an embed with a title and description specified by the user")
async def _embedshort(ctx, title, desc='.'):
    embed = discord.Embed(description=desc, title=title, color=ctx.author.color)
    await ctx.send(embed=embed)


@client.event
async def on_message(message):
    path = r"C:\Users\gigga.PAIGE\PycharmProjects\pythonProject\assets"
    os.chdir(r'C:\Users\gigga.PAIGE\PycharmProjects\pythonProject\assets')
    founddir = False
    if str(message.guild.id) in os.listdir(path):
        os.chdir(r'C:\Users\gigga.PAIGE\PycharmProjects\pythonProject\assets\{}'.format(message.guild.id))
        founddir = True
    if not founddir:
        os.mkdir(str(message.guild.id))
        os.chdir(r'C:\Users\gigga.PAIGE\PycharmProjects\pythonProject\assets\{}'.format(message.guild.id))
        open("usersText.json", "w+")
        f = open("usersText.json", "w")
        f.write('{}')
        f.close()
        open("levelallowed.txt", "w+")
        f = open("usersText.json", "w")
        f.write('True')
        f.close()
    if open("levelallowed.txt", 'r').read:

        if message.author == client.user:
            return

        author = message.author.name
        content = message.content
        channel = message.channel
        server = str(message.guild.name)

        print(f'''
        Server: {server}
            Channel: {channel}
                Author: {author}
                    Message: {content}
    ''')

        if not message.author.bot:
            await client.process_commands(message)
            with open('usersText.json', 'r') as f:
                users = json.load(f)
                await update_data(users, message.author)
                await add_exp(users, message.author, 5)
                await level_up(users, message.author, channel)
            with open('usersText.json','w') as f:
                json.dump(users, f)


async def update_data(users, user):
    if not await search(users, str(user.id)):
        users[str(user.id)] = {}
        users[str(user.id)]['exp'] = 0
        users[str(user.id)]['level'] = 1
        with open('usersText.json','w') as f:
            json.dump(users, f)


async def add_exp(users, user, exp):
    users[str(user.id)]['exp'] += exp


async def level_up(users, user, channel):
    exp = users[str(user.id)]['exp']
    lvl_start = users[str(user.id)]['level']
    lvl_end = int(exp ** (1/4))

    if lvl_start < lvl_end:
        await channel.send(f'{user.mention} has leveled up to level {lvl_end}!')
        users[str(user.id)]['level'] = lvl_end


async def search(values, searchFor):
    for k in values:
        if searchFor == k:
            return True
    return False

client.run(token)
