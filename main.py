import discord
from discord.ext import commands
import datetime
import requests
import random as rd

intents = discord.Intents.all()
intents.members = True
intents.typing = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith('!'):
        embed = discord.Embed(
        title = (f'**{message.author.name} used a command!**'),
        description = (f'{message.content}\n\n'
                       f'#{message.channel}'
                       ),
        color=0x9542f5,
        timestamp=datetime.datetime.utcnow()
        )
        log = discord.utils.get(message.guild.channels, name="log")
        await log.send(embed=embed)
        await bot.process_commands(message)
        return

@bot.command()
async def commands(ctx):
    embed = discord.Embed(
        title="**Commands list**",
        description="**!purge** - Use purge command to delete a large amount of message.\n"
        "**!ping** - Ping, Pong!\n"
        "**!cat** - Gives a random cat images. Meow :heart:"
        "**!rps** - Play Rock, Paper, Scissor with the bot."
        "**!coinflip** - Heads or Tails. :thinking:"
    )
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def cat(ctx):
     response = requests.get('https://api.thecatapi.com/v1/images/search')
     data = response.json()
     image_url = data[0]['url']
     embed = discord.Embed(title="Here's a cat for you! :cat:", color=0x00ff00)
     embed.set_image(url=image_url)
     await ctx.send(embed=embed)

@bot.command()
async def purge(ctx, amount: int = 0):
    if amount <= 0 or amount > 100:
        embedfail = discord.Embed(
        title = ("**Command: Purge**"),
        description = ('**Usage: **!purge [amount]\n'
                        '**Description: **Use purge command to delete a large amount of message. [100 limit]'
                      )
        )
        await ctx.send(embed=embedfail)
        return

    deleted = await ctx.channel.purge(limit=amount + 1)
    log = discord.utils.get(ctx.guild.channels, name="log")
    embeddelete = discord.Embed(
        title=("**Deletion Successful!**"),
        description= (f"Deleted **{len(deleted) - 1}** messages in #{ctx.channel}.")
    )

    await log.send(embed=embeddelete)

@bot.command()
async def rps(ctx, move: str = 'nil'):
    if move == 'nil':
        embedfail = discord.Embed(
            title="**Command: rps**",
            description="**Usage: ** !rps [Rock|Paper|Scissor]\n"
                        "**Description: ** use **rps** to play Rock, Paper, Scissor."
        )
        await ctx.send(embed=embedfail)
        return

    moves = {"rock": "Rock", "paper": "Paper", "scissor": "Scissor", "r": "Rock", "p": "Paper", "s": "Scissor"}
    if move.lower() not in moves:
        embedfail = discord.Embed(
            title="**Command: rps**",
            description="**Usage: ** !rps [Rock|Paper|Scissor]\n"
                        "**Description: ** use **rps** to play Rock, Paper, Scissor."
        )
        await ctx.send(embed=embedfail)
        return
    else:
        move = moves[move.lower()]

    RNG = rd.randint(1, 3)
    if RNG == 1:
        pick = "Rock"
    elif RNG == 2:
        pick = "Paper"
    elif RNG == 3:
        pick = "Scissor"

    if move == pick:
        draw = discord.Embed(
            title="**Draw**",
            description=f"Looks like we ended in a draw.\n"
                        f"I picked **{pick}** just like you!"
        )
        await ctx.send(embed=draw)
    elif (move == "Rock" and pick == "Scissor") or (move == "Paper" and pick == "Rock") or (move == "Scissor" and pick == "Paper"):
        win = discord.Embed(
            title="**You win!**",
            description=f"Wow! You picked **{move}** and I picked **{pick}**!\n"
                        f"Congratulations, you win!"
        )
        await ctx.send(embed=win)
    else:
        lose = discord.Embed(
            title="**You lose!**",
            description=f"It looks like you picked **{move}** and I picked **{pick}**!\n"
                        f"Sorry, better luck next time!"
        )
        await ctx.send(embed=lose)

@bot.command()
async def coinflip(ctx):
    if rd.randint(1,2) == 1:
        ht = "Heads"
    elif rd.randint(1,2) == 2:
        ht = "Tails"
    else:
        return

    embed = discord.Embed(
        title=f"{ctx.author.name} flipped a coin and got **{ht}**"
    )

    await ctx.send(embed=embed)


bot.run("")
