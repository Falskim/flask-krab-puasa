import asyncio
from datetime import datetime, timedelta
from typing import Optional
import discord
from discord.ext import tasks
import os
from dotenv import load_dotenv
import module.image_generation as ImageGeneration
import module.util as Util

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')
TARGET_CHANNEL_ID = os.getenv('DISCORD_TARGET_CHANNEL_ID')

if not TOKEN or not GUILD_ID:
    raise Exception(
        "DISCORD_TOKEN and DISCORD_GUILD_ID must be defined first in .env")

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
intents.guilds = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

prefix = '!'


ENABLE_PUASA_FEATURE = True
ENABLE_SAHUR_FEATURE = True
ENABLE_TARAWIH_FEATURE = False


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    if ENABLE_PUASA_FEATURE:
        puasa_notification.start()

    if ENABLE_SAHUR_FEATURE:
        sahur_notification.start()

    if ENABLE_TARAWIH_FEATURE:
        tarawih_notification.start()

    # ONE TIME ONLY
    # await tree.sync(guild=discord.Object(id=GUILD_ID))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    channel = message.channel

    if message.content.startswith(f'{prefix}hello'):
        await channel.send('Hello World!')
    elif message.content.startswith(f'{prefix}puasa') and ENABLE_PUASA_FEATURE:
        day = Util.get_puasa_day()
        filepath = ImageGeneration.get_puasa_hari_ke_image(day)
        with open(filepath, 'rb') as f:
            print('Sending', filepath)
            await channel.send(file=discord.File(f))
    elif message.content.startswith(f'{prefix}sahur') and ENABLE_SAHUR_FEATURE:
        filepath = ImageGeneration.get_sahur_assets()
        with open(filepath, 'rb') as f:
            await channel.send(file=discord.File(f))
    elif message.content.startswith(f'{prefix}tarawih') and ENABLE_TARAWIH_FEATURE:
        day = Util.get_tarawih_day()
        filepath = ImageGeneration.get_tarawih_hari_ke_image(day)
        try:
            with open(filepath, 'rb') as f:
                await channel.send(file=discord.File(f))
        except:
            await channel.send('Invalid Day Param')


@tree.command(
    name="puasa",
    description="Krab Puasa Hari Ke",
    guild=discord.Object(id=GUILD_ID)
)
async def puasa_command(ctx, day: Optional[int]):
    if not ENABLE_PUASA_FEATURE:
        return

    if day == None:
        day = Util.get_puasa_day()

    filepath = ImageGeneration.get_puasa_hari_ke_image(day)
    with open(filepath, 'rb') as f:
        picture = discord.File(f)
        await ctx.response.send_message(file=picture)


@tree.command(
    name="sahur",
    description="Sahur reminder",
    guild=discord.Object(id=GUILD_ID)
)
async def sahur_command(ctx):
    if not ENABLE_SAHUR_FEATURE:
        return

    filepath = ImageGeneration.get_sahur_assets()
    with open(filepath, 'rb') as f:
        await ctx.response.send_message(file=discord.File(f))


@tree.command(
    name="tarawih",
    description="Keutamaan tarawih",
    guild=discord.Object(id=GUILD_ID)
)
async def tarawih_command(ctx, day: Optional[int]):
    if not ENABLE_TARAWIH_FEATURE:
        return

    if day == None:
        day = Util.get_tarawih_day()

    filepath = ImageGeneration.get_tarawih_hari_ke_image(day)
    print('Tarawih', filepath, day)
    try:
        with open(filepath, 'rb') as f:
            picture = discord.File(f)
            await ctx.response.send_message(file=picture)
    except:
        await ctx.response.send_message('Invalid Day Param')


@tasks.loop(hours=24)
async def puasa_notification():
    if TARGET_CHANNEL_ID:
        channel = client.get_channel(TARGET_CHANNEL_ID) or await client.fetch_channel(TARGET_CHANNEL_ID)
        day = Util.get_puasa_day()
        filepath = ImageGeneration.get_puasa_hari_ke_image(day)
        with open(filepath, 'rb') as f:
            picture = discord.File(f)
            await channel.send(file=picture)


@puasa_notification.before_loop
async def before_puasa_notification():
    for _ in range(60 * 60 * 24):  # loop the whole day

        now = datetime.now(tz=Util.get_timezone_info())
        target = now.replace(hour=4, minute=30, second=0)

        if now.hour == target.hour and now.minute == target.minute:
            print('Start puasa notification')
            return

        seconds_difference = Util.seconds_difference_between_datetime(
            now, target, 'Puasa countdown')
        await asyncio.sleep(seconds_difference)


@tasks.loop(hours=24)
async def sahur_notification():
    if TARGET_CHANNEL_ID:
        channel = client.get_channel(TARGET_CHANNEL_ID) or await client.fetch_channel(TARGET_CHANNEL_ID)
        filepath = ImageGeneration.get_sahur_assets()
        with open(filepath, 'rb') as f:
            file = discord.File(f)
            await channel.send(file=file)


@sahur_notification.before_loop
async def before_sahur_notification():
    for _ in range(60 * 60 * 24):

        now = datetime.now(tz=Util.get_timezone_info())
        target = now.replace(hour=3, minute=00, second=0)

        if now.hour == target.hour and now.minute == target.minute:
            print('Start sahur notification')
            return

        seconds_difference = Util.seconds_difference_between_datetime(
            now, target, 'Sahur countdown')
        await asyncio.sleep(seconds_difference)


@tasks.loop(hours=24)
async def tarawih_notification():
    if TARGET_CHANNEL_ID:
        channel = client.get_channel(TARGET_CHANNEL_ID) or await client.fetch_channel(TARGET_CHANNEL_ID)
        day = Util.get_tarawih_day()
        filepath = ImageGeneration.get_tarawih_hari_ke_image(day)
        try:
            with open(filepath, 'rb') as f:
                picture = discord.File(f)
                await channel.send(file=picture)
        except:
            print('Invalid file', filepath)


@tarawih_notification.before_loop
async def before_tarawih_notification():
    for _ in range(60 * 60 * 24):

        now = datetime.now(tz=Util.get_timezone_info())
        target = now.replace(hour=18, minute=30, second=0)

        if now.hour == target.hour and now.minute == target.minute:
            print('Start tarawih notification')
            return

        seconds_difference = Util.seconds_difference_between_datetime(
            now, target, 'Tarawih countdown')
        await asyncio.sleep(seconds_difference)


client.run(TOKEN)
