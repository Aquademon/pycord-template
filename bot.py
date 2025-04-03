import discord
from discord.ext import commands
import os
from loguru import logger
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Configure Loguru
logger.add("src/logs/bot.log", rotation="10 MB", level="INFO", format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(intents=intents)

@bot.event
async def on_ready():
    logger.info(f"Discord bot initialization successful. Logged in as: {bot.user} (ID: {bot.user.id})")
    logger.info("Beginning to load cogs from ./src/cogs/")
    
    cog_count = 0
    for filename in os.listdir("./src/cogs/"):
        if filename.endswith(".py"):
            try:
                bot.load_extension(f"src.cogs.{filename[:-3]}")
                cog_count += 1
                logger.info(f"Successfully loaded cog: {filename[:-3]} from {filename}")
            except Exception as e:
                logger.error(f"Failed to load cog '{filename[:-3]}' from {filename}. Error: {str(e)}")
                logger.debug(f"Full traceback for {filename[:-3]} loading failure:", exc_info=True)
    
    logger.success(f"Bot startup complete. Successfully loaded {cog_count} cogs.")
    logger.info(f"Connected to {len(bot.guilds)} servers | Serving {sum(g.member_count for g in bot.guilds)} users")

@bot.event
async def on_command_error(ctx, error):
    command_name = ctx.command.name if ctx.command else "Unknown"
    user = ctx.author
    guild = ctx.guild.name if ctx.guild else "DM"
    
    logger.error(f"Command error occurred in {guild}")
    logger.error(f"Command: {command_name} | User: {user} (ID: {user.id})")
    logger.error(f"Error type: {type(error).__name__} | Details: {str(error)}")

bot.run(TOKEN)
