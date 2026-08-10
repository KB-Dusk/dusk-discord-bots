import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def main():
    async with bot:
        await bot.load_extension('cogs.moderation')
        print('Moderation cog loaded')
        await bot.start(TOKEN)

@bot.event
async def on_ready():
    print(f'Admin bot is online as {bot.user}')

asyncio.run(main())