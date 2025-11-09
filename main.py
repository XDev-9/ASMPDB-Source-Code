import discord
import os
from discord.ext import commands
from discord.ui import Button, View

bot = commands.Bot(command_prefix="+", intents=discord.Intents.all())
extensions = ["Cogs.moderation", "Cogs.fun", "Cogs.economy", "Cogs.general"]
bot.remove_command('help')

@bot.event
async def setup_hook():
    print("Initializing cogs...")
    for extension in extensions:
        try:
            await bot.load_extension(extension)
            print(f"Loaded {extension} successfully.")
        except Exception as error:
            print(f"{extension} cannot be loaded. [{error}]")
     
    try:
        syncedCommands = await bot.tree.sync()
        print(f"Synced {len(syncedCommands)} commands...")
    except Exception as e:
        print(f"An error has occured while syncing commands! [{e}]")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="Cooldown", 
        description=f"Slow down! Try again in {error.retry_after:.1f} seconds.",
        color=discord.Color.orange())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="Insufficient permissions",
         description="You do **not** have permission to use this command!",
          color=discord.Color.dark_red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="Unknown command", description="That command does not exist.", color=discord.Color.dark_gray())
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="A wild error appeared!", 
        description=f"{error}", 
        color=discord.Color.dark_red())
        await ctx.send(embed=embed)

@bot.command(description="Loads the cogs, no Idea what you'll use this for.")
async def load(ctx, *selective):
    for extension in extensions:
        try:
            await bot.load_extension(extension)
            await ctx.send(f"{extension} was successfully loaded.")
        except Exception as error:
            await ctx.send(f"{extension} cannot be loaded. [{error}]")

@bot.command()
async def tts(ctx):
    await ctx.send("Hello, World!", tts=True)

@bot.command(description="Changes the prefix to whatever you desire. Default prefix is: +", alias="prefix")
async def changePrefix(ctx, newPrefix):
    bot.command_prefix = newPrefix
    await ctx.send(f"Changed command prefix to: {newPrefix}")

with open("token.txt", "r") as file:
    TOKEN = file.read().strip()
bot.run(TOKEN)