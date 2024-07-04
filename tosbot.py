import discord
import os
intents1 = discord.Intents.default()
intents1.members = True
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Context

client = commands.Bot(command_prefix = '-', intents = intents1)

# Bot key loaded from dotenv file
load_dotenv()
TOS_BOT_KEY = os.getenv("BOT_KEY")

# Name of important features of a server that get matched up on startup
ALIVE_ROLE_NAME = "Alive"
YES_REACTION_NAME = "tosdrip"

# Global variables are required so that on message the channel the message was
# sent in can be checked before commands are evaluated

# List of global variables instantiated so that code doesn't break
day_channel = None
whisper_channel = None
bmer = None
jailor = None
jailee = None
vamp_chat = None
vh_channels = []
mayor = None
bmed = None
revealed_mayor = False
day = False

### NON-COMMAND SET-UP FUNCTIONS
@client.event
async def on_ready():
    print('Get ready to TOS')

@client.event
async def on_message(message: str):
    if message.channel == jailor and alive in message.author.roles:
        await jailee.send(f'**Jailor**: {message.content}')
    elif message.channel == jailee and alive in message.author.roles:
        await jailor.send(f'**{message.author.nick}**: {message.content}')
    elif message.channel == vamp_chat and alive in message.author.roles:
        for channel in vh_channels:
            await channel.send(f'**Vampire**: {message.content}')
    
    else:
        await client.process_commands(message)

# Funcs that return booleans which determine which players can use certain 
# commands
def i_am_not_revealed_mayor(ctx: Context):
    if day and (mayor not in ctx.author.roles):
        return True
    elif day and revealed_mayor == False:
        return True
    return False

def not_bmed(ctx: Context):
    return ctx.author == bmed

def i_am_mayor(ctx: Context):
    return mayor in ctx.author.roles

### ADMINISTRATOR COMMANDS
@client.command()
@commands.has_permissions(administrator=True)
async def start(ctx: Context):
    """Sets up the bot allowing all commands to work"""

    global botyes
    botyes = discord.utils.find(lambda e: e.name == YES_REACTION_NAME, 
                                 ctx.guild.emojis)
    global alive
    alive = discord.utils.find(lambda r: r.name == ALIVE_ROLE_NAME, 
                               ctx.guild.roles)

# Next two commands are used to check the administrator has set the game up 
# correctly
@client.command()
@commands.has_permissions(administrator=True)
async def channels(ctx: Context):
    """Checks channels that need to be set"""
    await ctx.send("Checking channels that are yet to be set...")

    if day_channel is None:
        await ctx.send("Day chat not set.")
    else:
        await ctx.send(f'Day chat: {day_channel.mention}')
    
    if whisper_channel is None:
        await ctx.send("Whisper channel not set.")
    else:
        await ctx.send(f'Whisper channel: {whisper_channel.mention}')

    if bmer is None:
        await ctx.send("Blackmailer whisper channel not set.")
    else:
        await ctx.send(f'Blackmailer whisper channel: {bmer.mention}')

    if jailor is None:
        await ctx.send("Jailor chat not set.")
    else:
        await ctx.send(f'Jailor chat: {jailor.mention}')

    if jailee is None:
        await ctx.send("Jailee chat not set.")
    else:
        await ctx.send(f'Jailee chat: {jailee.mention}')

    if vamp_chat is None:
        await ctx.send("Vampire chat not set.")
    else:
        await ctx.send(f'Vampire chat: {vamp_chat.mention}')

    if not vh_channels:
        await ctx.send("Vampire hunter channels not set.")
    else:
        await ctx.send(f'''There is/are {len(vh_channels)} vampire hunter 
                       channel/s set:''')
        for channel in vh_channels:
            await ctx.send(f'{channel.mention}')

@client.command()
@commands.has_permissions(administrator=True)
async def roles(ctx: Context):
    """Checks roles that need to be set"""
    await ctx.send("Checking if roles are set...")
    if mayor is None:
        await ctx.send("No mayor set")
    else:
        await ctx.send(f'Mayor is **{mayor.name}**')
    
    if bmed is None:
        await ctx.send("No player blackmailed.")
    else:
        await ctx.send(f'{bmed.name} is blackmailed')

# Next group of commands allows the administrator to set the game up
@client.command(aliases=['setday'])
@commands.has_permissions(administrator=True)
async def setdaychat(ctx: Context):
    """Assigns a channel as the day chat. There can only be one. Assigning a 
    second channel will override the previous one."""
    global day_channel
    day_channel = ctx.channel
    await ctx.send("Day chat set!")

@client.command(aliases=['setwhisper'])
@commands.has_permissions(administrator=True)
async def setwhisperchannel(ctx: Context):
    """Assigns a channel as the whisper channel. There can only be one. 
    Assigning a second channel will override the previous one."""
    global whisper_channel
    whisper_channel = ctx.channel
    await ctx.send("Whisper channel set!")

@client.command(aliases=['setbmer'])
@commands.has_permissions(administrator=True)
async def setbmerchannel(ctx: Context):
    """Assigns a channel as the blackmailer's whisper channel, where they can 
    see all of the whispers happening. There can only be one. Assigning a second
      channel will override the previous one."""
    global bmer
    bmer = ctx.channel
    await ctx.send("Blackmailer whisper channel set!")

@client.command(aliases=['setjailor'])
@commands.has_permissions(administrator=True)
async def setjailorchat(ctx: Context):
    """Assigns a channel as the jailor channel, where they may send messages to 
    talk to their jailed target. There can only be one. Assigning a second 
    channel will override the previous one."""
    global jailor
    jailor = ctx.channel
    await ctx.send('Jailor chat set!')

@client.command(aliases=['setjailee'])
@commands.has_permissions(administrator=True)
async def setjaileechat(ctx: Context):
    """Assigns a channel as the jailed channel, where they may send messages to 
    talk to their jailed target. There can only be one. Assigning a second 
    channel will override the previous one."""
    global jailee
    jailee = ctx.channel
    await ctx.send('Jailee chat set!')

@client.command(aliases=['setvampchat'])
@commands.has_permissions(administrator=True)
async def setvampirechat(ctx: Context):
    """Assigns a channel as the day chat. There can only be one. Assigning a 
    second channel will override the previous one."""
    global vamp_chat
    vamp_chat = ctx.channel
    await ctx.send("Vampire chat set!")

# Vampire hunter channels set as list as there can be multiple
@client.command(aliases=['setvhchannel'])
@commands.has_permissions(administrator=True)
async def setvampirehunterchannel(ctx: Context):
    """Assigns a channel as a vampire hunter channel, where messages from the 
    vampire chat are sent. There can be more than one, adding another channel 
    simply updates the list of vampire hunter channels. If you wish to delete a 
    vampire hunter channel from the server, make sure you use the 
    -removevhchannel command first."""
    global vh_channels
    vh_channels.append(ctx.channel)
    await ctx.send("Vampire hunter channel added!")

# Since the set command doesn't override VH channels, a remove function is 
# required
@client.command(aliases=['removevhchannel'])
@commands.has_permissions(administrator=True)
async def removevampirehunterchannel(ctx: Context):
    """Removes a vampire hunter channel from the list of vampire hunter 
    channels."""
    global vh_channels
    if ctx.channel in vh_channels:
        vh_channels.remove(ctx.channel)
        await ctx.send("Vampire hunter channel removed!")
    else:
        await ctx.send("This channel is not a vampire hunter channel!")

@client.command()
@commands.has_permissions(administrator=True)
async def setmayor(ctx: Context, num: str):
    """Sets a player's numbered role to be the mayor, giving them the ability to
      reveal themself as mayor during day time."""
    global mayor
    if num.isnumeric() and 1 <= int(num) <= 15:
        mayor = discord.utils.get(ctx.guild.roles, name=num)
        await ctx.send(f"Mayor set as numbered role **{int(num)}**")
    else:
        await ctx.send(f"Must specify number between 1 and 15 inclusive")

# Functions the administrator will use in game
@client.command(aliases=['blackmail'])
@commands.has_permissions(administrator=True)
async def bm(ctx: Context, num: str):
    """Sets a player as blackmailed, preventing them from whispering. Enter '-bm
      reset' to remove blackmailed person, or set another person to be 
      blackmailed to override the previous blackmailed player."""
    global bmed
    if num.isnumeric() and 1 <= int(num) <= 15:
        for m in ctx.guild.members:
            for r in m.roles:
                if r.name == num:
                    bmed = m
                    await ctx.send(f'{num} is now blackmailed.')
                    break
    elif num == 'reset':
        bmed = None
        await ctx.send(f'No one is now blackmailed.')
    else:
        await ctx.send(f'Invalid input.')

@client.command()
@commands.has_permissions(administrator=True)
async def day(ctx: Context):
    """Switch on day-time commands (whispering, revealing as Mayor)"""
    global day
    day = True
    await ctx.send(f'Day-time commands switched on.')

@client.command()
@commands.has_permissions(administrator=True)
async def night(ctx: Context):
    """Switch off day-time commands (whispering, revealing as Mayor)"""
    global day
    day = False
    await ctx.send(f'Day-time commands switched off.')

# Failsafe commands for the administrator
@client.command()
@commands.has_permissions(administrator=True)
async def revealmayor(ctx: Context):
    """Failsafe command to silently reveal mayor if for some reason the player
    cannot reveal themself"""
    global revealed_mayor
    revealed_mayor = True
    await ctx.send(f'Mayor silently revealed.')

### PLAYER COMMANDS
@client.command()
@commands.check(i_am_mayor)
@commands.check(i_am_not_revealed_mayor)
async def reveal(ctx: Context):
    global revealed_mayor
    revealed_mayor = True
    await ctx.send("""You have revealed to the town that you are the Mayor! You 
                   may no longer be visited by the doctor or send or receive 
                   whispers.""")
    await day_channel.send(f"""**{ctx.author.nick}** has revealed themself as 
                           the Mayor!""")


@client.command(aliases=['w'])
@commands.has_role('Alive')
@commands.check(i_am_not_revealed_mayor)
@commands.check(not_bmed)
async def whisper(ctx: Context, player: str, *, message: str):
    """You must use the target's number, not their name. e.g. '-w 7 you suck' or
      '-whisper 14 shut up exe'"""

    target = None

    # Loop determining the target from the player number
    if player.isnumeric() and 1 <= int(player) <= 15:
        for m in ctx.guild.members:
            for r in m.roles:
                if r.name == player:
                    target = m
                    break
    else:
        await ctx.send('Invalid recipient. Use number of whisper target.')
        return

    if discord.utils.get(ctx.author.roles, name=player) is not None:
        await ctx.send("You can't whisper to yourself.")
        return
    elif discord.utils.get(target.roles, name='Dead') is not None:
        await ctx.send('''You cannot whisper to a dead person. Try Discord 
                       TOS\'s new Medium DLC to talk to the dead!''')
    elif (discord.utils.find(lambda r: r == mayor, target.roles) is not None 
          and revealed_mayor):
        await ctx.send('You cannot whisper to a revealed mayor.')
    elif discord.utils.get(target.roles, name='Alive') is None:
        await ctx.send('You cannot whisper to that person.')
    else:
        
        target_channel = discord.utils.find(lambda c: c.name == player, 
                                            ctx.guild.channels)
        await target_channel.send(f'''{target.mention} 
                                  **From {ctx.author.nick}**: {message}''')
        await whisper_channel.send(f'''**{ctx.author.nick}** has whispered 
                                   to **{target.nick}**''')
        if bmer is not None:
            await bmer.send(f'''From **{ctx.author.nick}** to **{target.nick}**:
                             {message}''')
        await ctx.message.add_reaction(botyes)

client.run(TOS_BOT_KEY)