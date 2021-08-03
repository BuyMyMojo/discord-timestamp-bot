import time
from datetime import datetime, timezone, timedelta

import discord
import discord.ext.commands.errors
from discord.ext import commands
from discord.ext.commands import *

from secret_keys import *

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='->', description='', intents=intents, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False))
# bot.remove_command('help') this will help us make own help command
bot_version = 1.0

default_message_protection = discord.AllowedMentions(everyone=False, roles=False)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Prefix is ` | Use `help"))
    print("Online")


@bot.command(name="shutdown_bot", description="Shuts down the bot", help="Requires permission in the bot files")
async def shutdown_bot(ctx):
    role_names = [role.name for role in ctx.author.roles]  # List comp for getting the roles of the person doing command
    if bot_control_role in role_names or ctx.message.author.id in bot_admins:
        await ctx.send('Exiting now!')
        exit(420)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandOnCooldown):
        await ctx.send(f'You are on cooldown try again in {round(error.retry_after, 1)} seconds, moron! ')
    elif isinstance(error, MissingPermissions):
        await ctx.send('You do not have the required permissions for this command (loser!)!')
    elif isinstance(error, MemberNotFound):
        await ctx.send('You need to specify an actual member like this -command @[member]')
    elif isinstance(error, BadArgument):
        await ctx.send('You need to provide the correct argument type (a number or word)')
    else:
        raise error


@bot.event
async def on_message(message):
    message2 = message.content.casefold()
    if message.author == bot.user:
        return
    if message.author.bot:
        return
    await bot.process_commands(message)


@bot.command(name="timestamp_now", description="Generates timestamp for the current time", help="Simple example timestamp")
async def timestamp_now(ctx):
    unix = int(time.time())
    await ctx.send(f"Timestamp: <t:{unix}>\nRaw: `<t:{unix}>`")


@bot.command(name="timestamp", description="Generates timestamp from time info", help="Takes a timezone, day, month, year, hour, minutes and optionally style to generate a timestamp for use in discord")
async def timestamp(ctx, utc: float, day: int, month: int, year: int, hour: int, minute: int, style: str = None):
    dt = datetime(year, month, day, hour, minute, 0, 0, timezone(timedelta(hours=utc)))
    unix = int(dt.timestamp())
    if style is None:
        await ctx.send(f"Timestamp: <t:{unix}>\nRaw: `<t:{unix}>`")
    elif style == "short_time":
        await ctx.send(f"Timestamp: <t:{unix}:t>\nRaw: `<t:{unix}:t>`")
    elif style == "long_time":
        await ctx.send(f"Timestamp: <t:{unix}:T>\nRaw: `<t:{unix}:T>`")
    elif style == "short_date":
        await ctx.send(f"Timestamp: <t:{unix}:d>\nRaw: `<t:{unix}:d>`")
    elif style == "long_date":
        await ctx.send(f"Timestamp: <t:{unix}:D>\nRaw: `<t:{unix}:D>`")
    elif style == "short_date_time":
        await ctx.send(f"Timestamp: <t:{unix}:f>\nRaw: `<t:{unix}:f>`")
    elif style == "long_date_time":
        await ctx.send(f"Timestamp: <t:{unix}:F>\nRaw: `<t:{unix}:F>`")
    elif style == "relative_time":
        await ctx.send(f"Timestamp: <t:{unix}:R>\nRaw: `<t:{unix}:R>`")
    else:
        await ctx.send("Supported style formats:\n'short_time'\n'long_time'\n'short_date'\n'long_date'\n'short_date_time'\n'long_date_time'\n'relative_time'\nRemember to type them in without the ''")


bot.run(bot_token)
