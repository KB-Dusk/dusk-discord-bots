import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()
TOKEN = os.getenv('TOKEN')

print(f'Token loaded: {TOKEN is not None}')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')

async def main():
    print('Starting bot...')
    async with bot:
        print('Loading extension...')
        await bot.load_extension('cogs.moderation')
        print('Extension loaded, connecting to Discord...')
        await bot.start(TOKEN)

asyncio.run(main())