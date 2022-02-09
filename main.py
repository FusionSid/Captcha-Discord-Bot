import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(command_prefix="-")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(f"On {len(client.guilds)} servers! | -help"))
    print("Bot is online")

client.load_extension("cogs.captchabot")
client.load_extension("cogs.info")
client.load_extension("cogs.events")

client.run(os.environ["TOKEN"])