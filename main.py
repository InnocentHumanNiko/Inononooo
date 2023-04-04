import discord
from discord.ext import commands
import datetime
import requests

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

bot.run("MTA5Mjc5MzY5MTA1MzI0ODUzMg.G5mWri.uc_G27be2CZIE9rjCqfu7-INSUHvFJv8v2eqqE")