import discord
from discord.ext import commands
import os
from loguru import logger
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Configure Loguru
logger.add("src/logs/bot.log", rotation="10 MB", level="INFO", format="{time} - {level} - {message}")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(intents=intents)


# Load cogs function
@bot.event
async def on_ready():
    logger.info(f"Bot logged in as {bot.user}!")
    for filename in os.listdir("./src/cogs/"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")
    logger.info("Bot started!")

# Error handling
@bot.event
async def on_command_error(ctx, error):
    logger.error(f"Error: {error}")

bot.run(TOKEN)
