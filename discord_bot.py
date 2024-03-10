import asyncio
from datetime import datetime, timedelta
from typing import Optional
import discord
from discord.ext import tasks
import os
from dotenv import load_dotenv
import pytz
import image_generation as ImageGeneration
import util as Util

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')
TARGET_CHANNEL_ID = os.getenv('DISCORD_TARGET_CHANNEL_ID')

SAHUR_HOUR = 4

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


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    sahur_notification.start()
    # await tree.sync(guild=discord.Object(id=GUILD_ID))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(f'{prefix}hello'):
        await message.channel.send('Hello World!')
    elif message.content.startswith(f'{prefix}puasa'):
        day = Util.get_puasa_day()
        filepath = ImageGeneration.generate_puasa_hari_ke_image(day)
        with open(filepath, 'rb') as f:
            picture = discord.File(f)
            await message.channel.send(file=picture)


@tree.command(
    name="puasa",
    description="Krab Puasa Hari Ke",
    guild=discord.Object(id=GUILD_ID)
)
async def first_command(ctx, day: Optional[int]):
    if day == None:
        day = Util.get_puasa_day()

    filepath = ImageGeneration.generate_puasa_hari_ke_image(day)
    with open(filepath, 'rb') as f:
        picture = discord.File(f)
        await ctx.response.send_message(file=picture)


@tasks.loop(hours=24)
async def sahur_notification():
    if TARGET_CHANNEL_ID:
        channel = client.get_channel(TARGET_CHANNEL_ID) or await client.fetch_channel(TARGET_CHANNEL_ID)
        day = Util.get_puasa_day()
        filepath = ImageGeneration.generate_puasa_hari_ke_image(day)
        with open(filepath, 'rb') as f:
            picture = discord.File(f)
            await channel.send(file=picture)


@sahur_notification.before_loop
async def before_msg1():
    for _ in range(60 * 60 * 24):  # loop the whole day
        if datetime.now(tz=Util.get_timezone_info()).hour == SAHUR_HOUR:  # 24 hour format
            print('It is time')
            return
        await asyncio.sleep(1)
        # await asyncio.sleep(seconds_until_sahur())


def seconds_until_sahur():
    now = datetime.now(tz=Util.get_timezone_info())
    target = (now + timedelta(days=1)).replace(hour=SAHUR_HOUR,
                                               minute=0, second=0, microsecond=0)
    diff = (target - now).total_seconds()
    print(f"Sahur seconds : {target} - {now} = {diff}")
    return diff


client.run(TOKEN)
